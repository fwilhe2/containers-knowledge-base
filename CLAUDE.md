# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Two things in one repo:

1. `README.md` — a curated link collection about Linux container internals.
2. An Ansible playbook that provisions a "Linux Containers Lab" machine by **building the entire container stack from source** (runc, crun, podman, containerd, cri-o, conmon, skopeo, bubblewrap, netavark, aardvark-dns, passt, slirp4netns, rootlesskit, CNI plugins, ctop, ignite), plus a lima VM definition to run it in.

No application code is developed here — the repo is the build recipe plus smoke tests.

## Commands

```bash
# Normal workflow: everything runs inside the lima VM, never on the host
make vm         # create (if needed) and start the Debian 13 lab VM
make provision  # run the playbook inside it — builds the whole stack, slow
make test       # pytest the smoke tests inside it
make shell      # shell into the VM
make stop / make delete

# What `make provision` runs inside the guest (also exactly what CI runs)
ansible-playbook -v --inventory "localhost," --connection=local playbook.yaml

# Only re-clone the source repos, skip the builds
ansible-playbook --inventory "localhost," --connection=local playbook.yaml --tags containers

# Sync the forks with upstream (needs `gh` authenticated)
python3 update-forks.py

# Format README.md and *.yml with prettier
./format-files.sh

# Single smoke test (inside the VM)
pytest vm-resources/test-scripts/test_tools_installed.py -k podman   # single case
pytest vm-resources/test-scripts/test_crun.py                        # single file
```

The playbook needs `ansible` (full distribution, for `community.general.make`), `git`, `python3-apt`, `build-essential`, and `sudo`. **Never run it on the host**: it installs a long list of apt packages, enables a backports repo, and `make install`s binaries into `/usr/local`. Use the VM or the CI container.

## Architecture

**Source of truth is `git-repos.txt`.** Each line is cloned to `~/code/<url-path>` (shallow, `depth: 1`) and every later task refers to that path. Almost all are forks under `github.com/fwilhe-containers`, landing in `~/code/fwilhe-containers/<name>`. Upstream is forked deliberately so its main branch can be frozen — an upstream change that breaks the playbook only lands when `update-forks.py` runs, which `update.yml` does weekly (Sun 07:00 UTC) with the `PAT` secret.

The one exception is **passt**, which is not on GitHub: it is cloned straight from `passt.top` and therefore lands in `~/code/passt`, not under `fwilhe-containers/`. `update-forks.py` filters to `netloc == 'github.com'` for exactly this reason — `gh repo sync` cannot handle it.

Not everything cloned is built: `cni`, `systemd`, and `nodejs-container-image-builder` are checked out for reading only.

**`playbook.yaml` is order-dependent and has no roles.** A flat task list where apt build-dependency tasks are interleaved just before the builds needing them. Build style varies per project and must match upstream's:

- most: `community.general.make` (build), then again with `target: install` **and `become: true`**
- crun, slirp4netns: `./autogen.sh && ./configure` via shell first
- bubblewrap: `meson`, not make — and its setup step must tolerate an existing `_builddir`, or a second `make provision` fails
- netavark, aardvark-dns: Rust; their Makefiles wrap cargo and install into `/usr/local/libexec/podman`
- CNI plugins: `./build_linux.sh`, then binaries copied to `/usr/local/libexec/cni`
- ctop, ignite: non-default make targets / params
- runc: needs `RUNC_BUILDTAGS: "-libpathrs"` (see gotchas)

**The podman 5 networking stack is netavark + aardvark-dns + pasta**, all built from source. podman 5 dropped CNI, so it will not find helpers under `libexec/cni`; it searches `libexec/podman`. The CNI plugins are still built anyway — **cri-o** still uses them. slirp4netns is likewise still built even though podman now reaches for pasta.

**Two workflows run the same playbook, and they catch different things.**

- `.github/workflows/ci.yml` — `debian:13` container, ~20 min. Fast, but runs as **root** with no kernel and no systemd, so it can only assert each binary answers `--version`.
- `.github/workflows/ci-lima.yml` — the real VM via `make vm` / `make provision` / `make test`, ~30 min. Uses `lima-vm/lima-actions/setup@v1`, which installs qemu and chowns `/dev/kvm` (nested virt works on public-repo runners). This is the only place the tools actually *run*: podman pulls and runs a container, skopeo syncs an image, and pytest drives a full crun lifecycle. It is also the only place that exercises the **unprivileged-user** path.

The playbook must therefore stay Debian/Ubuntu-agnostic and must not assume systemd — the container has none, which is why the console-socket tasks are guarded by `when: ansible_service_mgr == 'systemd'`.

**`container-lab.yaml`** inherits digest-pinned Debian images from lima's own `template:_images/debian-13`, so image updates come from upgrading lima. It deliberately mounts nothing by default; `make vm` adds a single read-only mount of the checkout via `limactl create --mount "$(CURDIR)"`, which lands at the *same path* in the guest — safe only because lima gives the guest a `/home/<user>.guest` home that can never collide with the guest's own `~/code`. The `make` targets rely on that identical path via `limactl shell --workdir`. Template provisioning installs prerequisites only; the playbook runs from `make provision` so VM creation stays fast and the long build is retryable without recreating the VM. Its readiness probe waits for cloud-init, or `make provision` races apt for the dpkg lock.

When adding a tool: add the URL to `git-repos.txt`, add its build-deps + build + install tasks in dependency order, add a `--version` check to `ci.yml`, and add the same check to both `vm-resources/test-scripts/versions.sh` and `test_tools_installed.py` — those three lists duplicate each other and must stay in sync. The pytest files are not wired into the Docker job; they run via `make test`, which the lima job calls.

## Gotchas

- **A missing `become: true` on an install task passes Docker CI and fails everywhere real.** Docker runs as root, so writes to `/usr/local` succeed there and only blow up in the VM. When touching install steps, check `become` explicitly rather than trusting a green Docker run.
- **The forks drift.** They sync weekly against a CI that was red from Aug 2025 to Aug 2026, so upstream had a year to move. Expect build breaks unrelated to your change, and read the actual upstream Makefile/configure rather than guessing: runc made `libpathrs` a default build tag that nothing packages, crun swapped yajl for json-c, netavark needs `protoc` at build time.
- **Rust comes from backports.** netavark and aardvark-dns declare `rust-version = 1.88`; trixie ships 1.85. `default_release` is scoped to `rustc`/`cargo` only — widening it would silently pull unrelated packages from backports.
- **gvisor/runsc is disabled in three places** and must be re-enabled together: the commented bazel tasks in `playbook.yaml`, the `runsc --version` line in `ci.yml`, and the commented entries in `versions.sh` and `test_tools_installed.py`.
- **`test_crun.py` needs a live console socket.** It runs `crun create --console-socket=mySocket.sock` with cwd `~/code/fwilhe-containers/container-image` (the OCI bundle built by the playbook). `vm-resources/container-socket.service` provides it; the playbook installs it as a systemd **user** unit (`%h`, no `User=`) with lingering enabled, so `make test` works without manual setup.
- **`format-files.sh` does not touch `playbook.yaml`** — it globs `*.yml`, and the playbook uses the `.yaml` extension.
- The playbook has no `deb-src` / `apt build-dep` step; the one that existed served the systemd build removed in `2284ce4` and pinned Ubuntu jammy, which would have broken the Debian guest.

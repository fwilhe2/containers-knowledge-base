# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Two things in one repo:

1. `README.md` — a curated link collection about Linux container internals.
2. An Ansible playbook that provisions a "Linux Containers Lab" machine by **building the entire container stack from source** (runc, crun, podman, containerd, cri-o, conmon, skopeo, bubblewrap, slirp4netns, rootlesskit, CNI plugins, ctop, ignite), plus a lima VM definition to run it in.

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

# Sync all forks in the fwilhe-containers org with upstream (needs `gh` authenticated)
python3 update-forks.py

# Format README.md and *.yml with prettier
./format-files.sh

# Single smoke test (inside the VM)
pytest vm-resources/test-scripts/test_tools_installed.py -k podman   # single case
pytest vm-resources/test-scripts/test_crun.py                        # single file
```

The playbook needs `ansible` (full distribution, for `community.general.make`), `git`, `python3-apt`, `build-essential`, and `sudo`. **Never run it on the host**: it installs a long list of apt packages and `make install`s binaries into `/usr/local`. Use the VM or the CI container.

## Architecture

**Source of truth is `git-repos.txt`.** Every line is a fork under `github.com/fwilhe-containers`. The playbook clones each into `~/code/fwilhe-containers/<repo-name>` (shallow, `depth: 1`) and every later task refers to that path. Upstream projects are forked deliberately so their main branch can be frozen — an upstream change that breaks the playbook only lands when `update-forks.py` is run. `update.yml` runs that script weekly (Sun 07:00 UTC) using the `PAT` secret.

Not everything cloned is built: `cni`, `systemd`, and `nodejs-container-image-builder` are checked out for reading/experimentation only.

**`playbook.yaml` is order-dependent and has no roles.** It is a flat task list where apt build-dependency tasks are interleaved just before the build tasks that need them. Build style varies per project and must match upstream's:

- most: `community.general.make` (build), then again with `target: install` and `become: true`
- crun, slirp4netns: `./autogen.sh && ./configure` via shell first
- bubblewrap: `meson` (compile/test/install), not make
- CNI plugins: `./build_linux.sh`, then binaries copied to `/usr/local/libexec/cni`
- ctop, ignite: non-default make targets / params

When adding a tool: add the fork URL to `git-repos.txt`, add its build-deps + build + install tasks in dependency order, add a `--version` check to `.github/workflows/ci.yml`, and add the same check to both `vm-resources/test-scripts/versions.sh` and `test_tools_installed.py`.

**Two environments run the same playbook.** `.github/workflows/ci.yml` runs it inside an `ubuntu:24.10` container as root and asserts each built binary answers `--version`; `container-lab.yaml` + `Makefile` run it inside a Debian 13 lima VM. The playbook must therefore stay distro-agnostic across Debian/Ubuntu and must not assume systemd — the container has none, which is why the console-socket tasks at the end are guarded by `when: ansible_service_mgr == 'systemd'`.

**`container-lab.yaml`** inherits digest-pinned Debian images from lima's own `template:_images/debian-13`, so image updates come from upgrading lima. It deliberately mounts nothing by default; `make vm` adds a single read-only mount of the checkout via `limactl create --mount "$(CURDIR)"`, which lands at the *same path* in the guest — safe only because lima gives the guest a `/home/<user>.guest` home that can never collide with the guest's own `~/code`. The `make` targets rely on that identical path via `limactl shell --workdir`. Provisioning in the template installs prerequisites only; the playbook runs from `make provision` so VM creation stays fast and the long build is retryable without recreating the VM.

When adding a tool: add the fork URL to `git-repos.txt`, add its build-deps + build + install tasks in dependency order, add a `--version` check to `.github/workflows/ci.yml`, and add the same check to both `vm-resources/test-scripts/versions.sh` and `test_tools_installed.py` — those three lists duplicate each other and must stay in sync. The pytest files are not wired into CI; they run via `make test`.

## Gotchas

- **gvisor/runsc is disabled in three places** and must be re-enabled together: the commented bazel tasks in `playbook.yaml`, the `runsc --version` line in `ci.yml`, and the commented entries in `versions.sh` and `test_tools_installed.py`.
- **`test_crun.py` needs a live console socket.** It runs `crun create --console-socket=mySocket.sock` with cwd `~/code/fwilhe-containers/container-image` (the OCI bundle built by the playbook). `vm-resources/container-socket.service` provides it; the playbook installs it as a systemd **user** unit (`%h`, no `User=`) and starts it, so `make test` works without manual setup.
- **`format-files.sh` does not touch `playbook.yaml`** — it globs `*.yml`, and the playbook uses the `.yaml` extension.
- The playbook has no `deb-src` / `apt build-dep` step any more; the one that existed served the systemd build removed in `2284ce4` and pinned Ubuntu jammy, which would have broken the Debian guest.

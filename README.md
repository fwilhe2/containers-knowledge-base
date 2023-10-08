# Containers Knowledge-Base

Collection of knowledge on containers 🐋📦

## Basics

- [All things Linux containers](http://containerz.info/)
- [Containers Resources](https://github.com/cloudfoundry/garden-runc-release/wiki/Containers-Resources)
- [Awesome Linux Containers](https://github.com/Friz-zy/awesome-linux-containers)
- [Awesome Immutable](https://github.com/castrojo/awesome-immutable)
- [What Is a Standard Container (2021 edition)](https://iximiuz.com/en/posts/oci-containers/)
- [lwn: Docker and the OCI container ecosystem](https://lwn.net/Articles/902049/)

### [Namespaces](https://en.wikipedia.org/wiki/Linux_namespaces)

[Digging into Linux namespaces](https://blog.quarkslab.com/digging-into-linux-namespaces-part-1.html)

### [cgroups](https://en.wikipedia.org/wiki/Cgroups)

- [Introduction to cgroups](https://0xax.gitbooks.io/linux-insides/content/Cgroups/linux-cgroups-1.html)
- [Cgroups - Deep Dive into Resource Management in Kubernetes](https://martinheinz.dev/blog/91)

Copy-on-write filesystems

- [image-spec](https://github.com/opencontainers/image-spec)
- [distribution-spec](https://github.com/opencontainers/distribution-spec)
- [runtime-spec](https://github.com/opencontainers/runtime-spec)

## Software

- [Docker](https://github.com/docker/cli)
- [Podman](https://github.com/containers/podman)
- [CRI-O](https://github.com/cri-o/cri-o)
- [bubblewrap](https://github.com/containers/bubblewrap)/flatpak
- [containerd](https://github.com/containerd/containerd)
- [systemd-nspawn](https://www.freedesktop.org/software/systemd/man/systemd-nspawn.html)
- [runc](https://github.com/opencontainers/runc)
- [crun](https://github.com/containers/crun)

## Container Images

### Building Images

#### Dockerfile/Containerfile

Layering, Builder Pattern, Multi-Arch builds

## Running Containers

### [Rootless Containers](https://rootlesscontaine.rs/)

## Playground Environment

[`container-lab.yaml`](./container-lab.yaml) provides a reproducible development environment built via [an Ansible playbook](./playbook.yaml).

So far there is not much to see there, but the vision is to produce an environment with all needs to tinker with container software, to change it and to learn about it.

It's built using [lima](https://github.com/lima-vm/lima/).
The `Makefile` has some shortcuts for using it.

This can be used with the [ssh remote plugin for vs code](https://code.visualstudio.com/docs/remote/ssh) to work with the repos inside the vm.

Configuration for vs code ssh remote plugin:

You need a local ssh key for this.

Run the following command to allow easy access:

```
echo "Include ${LIMA_HOME:-$HOME/.lima}/container-lab-vm/ssh.config" >> ~/.ssh/config
```

After this you can connect to the host `lima-container-lab-vm`.

## Talks

[Containers at Facebook - Lindsay Salisbury](https://youtu.be/_Qc9jBk18w8)

systemd, BTRFS, ...

https://www.cyphar.com/blog/post/20190121-ociv2-images-i-tar

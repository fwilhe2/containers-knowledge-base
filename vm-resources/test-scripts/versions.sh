#!/bin/bash
# Single source of truth for the "is it installed and does it run" checks, used
# by the Docker CI job. Anything needing a real system (podman info, the crun
# lifecycle) lives in the pytest suite instead, which only the lima job runs.
#
# set -e matters: without it every failure here was silently discarded.
set -euxo pipefail

bwrap --version
conmon --version
containerd --version
crio --version
crun --version
ctop -v
ignite version
podman --version
rootlesskit --version
runc --version
# runsc --version
skopeo --version
# netavark and aardvark-dns install into libexec/podman, deliberately not on PATH.
/usr/local/libexec/podman/netavark --version
/usr/local/libexec/podman/aardvark-dns --version
pasta --version

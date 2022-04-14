echo "::group::Version Info"
conmon --version
containerd --version
crio --version
crun --version
podman --version
podman info
rootlesskit --version
runc --version
runsc --version
skopeo --version
echo "::endgroup::"

echo "::group::Podman Info"
podman info
echo "::endgroup::"

echo "::group::Podman Hello"
podman run quay.io/podman/hello
echo "::endgroup::"
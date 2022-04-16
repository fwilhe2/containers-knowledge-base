echo "::group::Version Info"
bwrap --version
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

pushd ~/code/fwilhe-containers/container-image
nc -lkU mySocket.sock &
crun create --console-socket=mySocket.sock myContainer
crun list --format=json
crun --debug state myContainer
crun start myContainer
crun list --format=json
crun --debug state myContainer

popd
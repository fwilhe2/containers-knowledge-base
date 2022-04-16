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

echo "::group::Test lifecycle of a container with crun/runc"
pushd ~/code/fwilhe-containers/container-image
nc -lkU mySocket.sock &
sudo DEBIAN_FRONTEND=noninteractive apt-get -y install python3-pip
sudo pip --no-input install pytest
pytest -svv
popd
echo "::endgroup::"

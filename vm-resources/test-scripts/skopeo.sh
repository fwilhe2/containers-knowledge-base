mkdir -p ~/container-images
skopeo sync --src docker --dest dir quay.io/podman/hello ~/container-images
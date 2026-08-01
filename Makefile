VM ?= container-lab

.PHONY: vm provision test shell stop delete format

## Create (if needed) and start the lab VM, with this checkout mounted read-only.
## Lima mounts it at the same path it has on the host, so $(CURDIR) is also the
## guest-side path used by the targets below.
vm:
	limactl list --quiet | grep -qx '$(VM)' || \
		limactl create --tty=false --name='$(VM)' --mount '$(CURDIR)' container-lab.yaml
	limactl start '$(VM)'

## Build and install the whole container stack inside the VM. Takes a long time.
provision:
	limactl shell --workdir '$(CURDIR)' '$(VM)' \
		ansible-playbook -v --inventory "localhost," --connection=local playbook.yaml

## Run the smoke tests inside the VM (requires `make provision` first).
## The checkout is mounted read-only, so pytest cannot write its cache.
test:
	limactl shell --workdir '$(CURDIR)/vm-resources/test-scripts' '$(VM)' \
		python3 -m pytest -sv -p no:cacheprovider

shell:
	limactl shell '$(VM)'

stop:
	limactl stop '$(VM)'

delete:
	limactl delete --force '$(VM)'

format:
	./format-files.sh

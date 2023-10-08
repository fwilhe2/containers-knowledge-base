build:
	cat container-lab.yaml | limactl create --name=container-lab-vm -

start:
	limactl start container-lab-vm

shell:
	limactl shell container-lab-vm

stop:
	limactl stop container-lab-vm

delete:
	limactl delete container-lab-vm

playbook:
	ansible-playbook -v --inventory "localhost," --connection=local playbook.yaml
	cp vm-resources/container-socket.service /etc/systemd/system/container-socket.service
	systemctl enable container-socket.service
	systemctl start container-socket.service
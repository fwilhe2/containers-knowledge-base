Vagrant.configure(2) do |config|
  config.vm.box = "generic/ubuntu2204"

  config.vm.synced_folder ".", "/vagrant", disabled: false

  config.vm.provider 'libvirt' do |provider|
    provider.memory = 4096
    provider.cpus = 8
  end

  config.vm.provider "virtualbox" do |provider|
    provider.memory = 4096
    provider.cpus = 8
  end

  config.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "playbook.yaml"
      ansible.compatibility_mode = "2.0"
      ansible.raw_arguments = [
          '-vv'
      ]
  end

  # Install non-container related convinience tools to the vm
  config.vm.provision "shell", inline: "apt-get install -yqq jq"

  config.vm.provision "file", source: "vm-resources", destination: "/home/vagrant"
  config.vm.provision "shell", inline: "cp container-socket.service /etc/systemd/system/container-socket.service && sudo systemctl enable container-socket.service"

  # Pytest for running tests
  config.vm.provision "shell", inline: "DEBIAN_FRONTEND=noninteractive apt-get -yqq install python3-pip && pip --no-input install pytest"

  config.vm.provision :shell do |shell|
    shell.privileged = true
    shell.inline = 'echo rebooting after provisioning'
    shell.reboot = true
  end
end
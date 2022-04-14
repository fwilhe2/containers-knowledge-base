Vagrant.configure(2) do |config|
  config.vm.box = "generic/ubuntu2110"

  config.vm.synced_folder ".", "/vagrant", disabled: false

  config.vm.provider 'libvirt' do |provider|
    provider.memory = 1024
    provider.cpus = 2
  end

  config.vm.provider "virtualbox" do |provider|
    provider.memory = 4096
    provider.cpus = 8
  end

  config.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "playbook.yaml"
      ansible.compatibility_mode = "2.0"
      ansible.raw_arguments = [
          '-vvvv'
      ]
  end

  config.vm.provision :shell do |shell|
    shell.privileged = true
    shell.inline = 'echo rebooting after provisioning'
    shell.reboot = true
  end

  config.vm.provision "shell", path: "run-tools.sh"

  config.vm.provision "file", source: "box-readme.md", destination: "readme.md"
end
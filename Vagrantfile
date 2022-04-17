Vagrant.configure(2) do |config|
  config.vm.box = "generic/ubuntu2110"

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

  config.vm.provision "file", source: "test-scripts/versions.sh", destination: "~/versions.sh"
  config.vm.provision "file", source: "test-scripts/podman.sh", destination: "~/podman.sh"
  config.vm.provision "file", source: "test-scripts/skopeo.sh", destination: "~/skopeo.sh"

  config.vm.provision :shell do |shell|
    shell.privileged = true
    shell.inline = 'echo rebooting after provisioning'
    shell.reboot = true
  end
end
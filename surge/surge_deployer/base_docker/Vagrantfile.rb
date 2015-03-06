# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'ipaddr'
require 'yaml'
# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

$vars = YAML::load_file("/Users/tokwii/Surge/example/pipeline.yml")
$provider = $vars['provider']['type']['docker']
$nodes = $vars['hosts']

$ansible_groups = {}
$hosts = $nodes.keys
start_port = $provider['start_port']
docker_host_ports = Array []

$hosts.each do | server |
  $ansible_groups.store(server , $nodes[server]["count"])
end 
puts $ansible_groups

### Create ansible inventory File ###########
File.open('ansible_docker_inventory' ,'w') do |f|
  
  $ansible_groups.each do | key , value |
      # Ansible groups 
      f.write "[#{key}]\n" 
      # Hosts    
      value.times do |k|
          docker_host_ports.push(start_port)
          f.write "localhost:#{start_port}\n"
          start_port = start_port + 20 
      end 
      f.write "\n"
  end 

end

#############################################
=begin
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.
	config.vm.define "trusty" do |v|
		v.vm.provider "docker" do |d|
			d.build_dir = "."
			d.has_ssh = true	
      d.ports = ["9000:22","8080:8080"]	
		end
		v.ssh.username = "root"
		v.ssh.password = "root"
		#v.vm.provision "shell" , inline:"echo Hello World !"
	end
  #config.vm.provision "shell" , inline:"echo Hello World !"
   config.vm.provision "ansible" do |ansible|
      ansible.playbook = "playbook/bootstrap.yml"
      ansible.sudo = true
      ansible.limit = 'all'
    end

end

=end




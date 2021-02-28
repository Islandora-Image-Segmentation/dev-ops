# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

$cpus   = ENV.fetch("ISLANDORA_VAGRANT_CPUS", "2")
$memory = ENV.fetch("ISLANDORA_VAGRANT_MEMORY", "3000")
$hostname = ENV.fetch("ISLANDORA_VAGRANT_HOSTNAME", "islandora")
$forward = ENV.fetch("ISLANDORA_VAGRANT_FORWARD", "TRUE")
$multiple_vms  = ENV.fetch("ISLANDORA_VAGRANT_MULTIPLE_ISLANDORAS", "FALSE")

Vagrant.require_version ">= 2.0.3"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.
  config.vm.provider "virtualbox" do |v|
    v.name = "Islandora 7.x-1.x Newspaper Development Base VM"
  end

  config.vm.synced_folder "./", "/vagrant", disabled:true
  config.vm.synced_folder "data/ingest/", "/data"
  config.vm.synced_folder "vagrant/", "/vagrant"

  config.vm.hostname = $hostname

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "bento/ubuntu-16.04"
  config.vm.box_version = "202005.21.0"


  # This checks and updates VirtualBox Guest Additions.
   if Vagrant.has_plugin?("vagrant-vbguest")
    config.vbguest.auto_update = true
    config.vbguest.no_remote = false
   end

  unless  $forward.eql? "FALSE"
    config.vm.network :forwarded_port, guest: 8080, host: 8080, id: 'Tomcat', auto_correct: true
    config.vm.network :forwarded_port, guest: 3306, host: 3306, id: 'MySQL', auto_correct: true
    config.vm.network :forwarded_port, guest: 8000, host: 8000, id: 'Apache', auto_correct: true
    config.vm.network :forwarded_port, guest: 22, host: 2222, id: "ssh", auto_correct: true
  end

  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--memory", $memory]
    vb.customize ["modifyvm", :id, "--cpus", $cpus]
  end

  config.vm.provider "hyperv" do |h|
    h.vmname = "Islandora 7.x-1.x Newspaper Development Base VM"
    h.cpus = $cpus
    h.memory = $memory
  end

  shared_dir = "/vagrant"
  data_dir = "/data"
  # Moves Islandora 7.x to ipaddress instead of localhost.
  unless  $multiple_vms.eql? "FALSE"
     unless Vagrant.has_plugin?("vagrant-hostsupdater")
       raise 'vagrant-hostsupdater is not installed!'
     end
     config.vm.network :private_network, ip: "33.33.33.10"

   end

  config.vm.provision :shell, inline: "sudo sed -i '/tty/!s/mesg n/tty -s \\&\\& mesg n/' /root/.profile", :privileged =>false
  config.vm.provision :shell, path: "./vagrant/scripts/java.sh", :args => shared_dir
  config.vm.provision :shell, path: "./vagrant/scripts/bootstrap.sh", :args => shared_dir
  config.vm.provision :shell, path: "./vagrant/scripts/devtools.sh", :args => shared_dir
  config.vm.provision :shell, path: "./vagrant/scripts/fits.sh", :args => shared_dir
  config.vm.provision :shell, path: "./vagrant/scripts/fcrepo.sh", :args => shared_dir
  config.vm.provision :shell, path: "./vagrant/scripts/djatoka.sh", :args => shared_dir
  config.vm.provision :shell, path: "./vagrant/scripts/solr.sh", :args => shared_dir
  config.vm.provision :shell, path: "./vagrant/scripts/gsearch.sh", :args => shared_dir
  config.vm.provision :shell, path: "./vagrant/scripts/drupal.sh", :args => shared_dir
  config.vm.provision :shell, path: "./vagrant/scripts/tesseract.sh", :args => shared_dir
  config.vm.provision :shell, path: "./vagrant/scripts/ffmpeg.sh", :args => shared_dir
  config.vm.provision :shell, path: "./vagrant/scripts/warctools.sh", :args => shared_dir
  config.vm.provision :shell, path: "./vagrant/scripts/sleuthkit.sh", :args => shared_dir
  config.vm.provision :shell, path: "./vagrant/scripts/cantaloupe.sh", :args => shared_dir
  config.vm.provision :shell, path: "./vagrant/scripts/post-base.sh"

  config.vm.provision :shell, path: "./vagrant/scripts/islandora_modules.sh", :args => shared_dir, :privileged => false
  config.vm.provision :shell, path: "./vagrant/scripts/islandora_libraries.sh", :args => shared_dir, :privileged => false
  config.vm.provision :shell, path: "./vagrant/scripts/ingest.sh", :args => [shared_dir, data_dir], :privileged => false
  if File.exist?("./scripts/custom.sh") then
    config.vm.provision :shell, path: "./scripts/custom.sh", :args => shared_dir
  end
  config.vm.provision :shell, path: "./vagrant/scripts/post.sh"

  unless  $multiple_vms.eql? "FALSE"
    # Fires last to modify one last change.
    config.vm.provision "this",
    type: "shell",
    preserve_order: true,
    inline: "cd /var/www/drupal && /usr/bin/drush vset islandora_paged_content_djatoka_url 'http://33.33.33.10:8080/adore-djatoka'"
  end
end

package {
	["telnet", "wget", "rsync", "bind-utils", "vim-enhanced", "system-config-network-tui", "lrzsz"]:
		ensure    => installed;
	["dhclient"]:
		provider => yum,
		ensure=>absent;
	"epel-release-6-7":
		ensure => present,
		provider => rpm,
		source=>"http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-7.noarch.rpm";
	"rpmforge-release-0.5.2-2.el6.rf":
		ensure => present,
                provider => rpm,
		source=>"http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.2-2.el6.rf.x86_64.rpm"
}


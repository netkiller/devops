node default { file { "/tmp/puppettest1.txt": content => "hello,first puppet manifest"; } }
import "pkgs.pp"
import "www.pp"
import "nodes.pp"

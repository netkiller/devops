node www {
    user {   "www":
      uid   => 80,
      shell => "/bin/bash",
      home  => "/www",
    }
    file { "/var/www":
        owner => "nginx",
        group => "nginx",
        mode => 700,
        ensure => directory;
    }

    file { "/var/www/index.html":
        source => "/tmp/something",
        mode   => 666;
    }
}

class users {

  # define the administrator group
  group { 'inprov':
    ensure => present,
    gid    => 2024,
  }

  # admin users
  user { 'jduggan':
  ensure     => present,
  uid        => '2305',
  gid        => '2024',
  groups     => ['inprov'],
  shell      => '/bin/bash',
  home       => '/home/jduggan',
  managehome => true,
  require    => Group['inprov'],
  }

  # sudo privileges for admin group
  file { '/etc/sudoers.d/admin':
  ensure  => file,
  owner   => 'root',
  group   => 'root',
  mode    => '0440',
  content => "%inprov ALL=(ALL) NOPASSWD: ALL\n",
  require => Group['inprov'],
  }

}

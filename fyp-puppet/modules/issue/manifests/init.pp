class issue {

  package { 'figlet':
    ensure  => installed,
  }

  file { '/etc/motd':
    ensure  => file,
    content => template('/etc/puppet/code/environments/production/modules/issue/templates/issue.erb'),
    require => Package['figlet'],
  }
}

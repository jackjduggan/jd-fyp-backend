class packages (
) {

  # docker
  package { 'docker.io':
    ensure => installed,
  }

  service { 'docker':
    ensure    => running,
    enable    => true,
    require   => Package['docker.io'],
  }

  # apache2
  $apache_package = $facts['os']['family'] ? {
    'RedHat'  => 'httpd',
    'Debian'  => 'apache2',
    default   => 'apache2',
  }

  $apache_service = $apache_package

  package { $apache_package:
    ensure => installed,
  }

  service { $apache_service:
    ensure    => running,
    enable    => true,
    require   => Package[$apache_package],
  }

  file { '/var/www/html/index.html':
    ensure  => file,
    mode    => '0644',
    content => template('/etc/puppet/code/environments/production/modules/packages/templates/index.html.erb'),
    notify  => Service[$apache_service],
    require => Package[$apache_package],
  }
}

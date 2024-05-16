#change user limits
exec { 'Fix Limit':
  command  => 'echo -e "holberton hard nofile 2500\nholberton soft nofile 25000" > /etc/security/limits.conf',
  provider => shell,
}

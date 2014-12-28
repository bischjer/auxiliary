#-*-auxscript-*-

from aux.device.linux import LinuxDevice


localsystem = LinuxDevice("localhost")

print localsystem.identifier

localsystem.ssh.set_credentials(('user', 'pass'))

print localsystem.ssh.cmd('ls -al')

print "hello"

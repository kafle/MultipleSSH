import pxssh
import optparse
from threading import *


def indentOutput(output):
  '''Indents output to distinguish between outputs from different hosts.'''

  return output.replace('\n', '\n  ')

def connect(host, user, password, command):
  '''Connects to hosts and runs a command. Most basic exception handling.'''

  try:
    s = pxssh.pxssh()
    s.login(host, user, password) # Attempt login
    print '\n[+] Logged into ' + user + '@' + host
    s.sendline(command)
    s.prompt()
    print '  [+] ' + host + ' says:'
    print '  ' + indentOutput(s.before)
    print '  [+] Logging out of ' + host + '.'
    s.logout()
  except Exception, e: # All exceptions interpreted as failed login.
    print '[-] Could not log into ' + host

def main():
  '''Parses arguments and spawns threads to do the actual connecting etc'''

  # Argument parser
  parser = optparse.OptionParser('usage%prog -H <target> -u <user> -F <dict file>')
  parser.add_option('-H', dest='hostF', type='string', help='Specify file with  <username>:<password>@<host name> on each line.')
  parser.add_option('-c', dest='command', type='string', help='Specify command to run on each connected host in quotes e.g. "ls -l".', default='hostname')
  (options, args) = parser.parse_args()

  # Check correct usage
  if options.hostF == None:
    print parser.usage
    exit(0)
  
  # Read host file, parse it and spawn threads
  fn = open(options.hostF, 'r')
  for line in fn.readlines():
    splitLine = line.strip('\r').strip('\n').split('@')
    username = splitLine[0].split(':')[0]
    password = splitLine[0].split(':')[1]
    hostname = splitLine[1]
    print '[+] Connecting to: ' + username + '@' + hostname 
    t = Thread(target=connect, args=(hostname, username, password, options.command))
    child = t.start()


if __name__ == '__main__':
  main()

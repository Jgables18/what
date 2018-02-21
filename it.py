import RoboPiLib as RPL
RPL.RoboPiInit("/dev/ttyAMA0",115200)
import sys, tty, termios, signal

# Definitions
# pin 1 = left
#500-1190

# pin 2 = right
#1810

def stopAll():
    pass

def open():
  RPL.servoWrite(0, 500)
  RPL.servoWrite(1, 2500)
  print "open"

def close():
  RPL.servoWrite(0, 1000)
  RPL.servoWrite(1, 2000)
  print "close"

i = RPL.servoRead(0)
j = RPL.servoRead(1)

def stepclose():
    RPL.servoWrite(0,i+10)
    RPL.servoWrite(1,j-10)
    print "step close"


fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

######################################
## Other motor commands should go here
######################################

def interrupted(signum, frame):
  stopAll()

signal.signal(signal.SIGALRM, interrupted)
tty.setraw(sys.stdin.fileno())

print "Ready To Grab! Press * to quit.\r"

SHORT_TIMEOUT = 0.255
while True:
  signal.setitimer(signal.ITIMER_REAL,SHORT_TIMEOUT)
  ch = sys.stdin.read(1)
  signal.setitimer(signal.ITIMER_REAL,0)
  if ch == '*':
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) # this resets the console settings
    break
  else:
    if ch == 'w':
      open()
    elif ch == "a":
      close()
    elif ch == "s":
      stepclose()
    else:
      stopAll()

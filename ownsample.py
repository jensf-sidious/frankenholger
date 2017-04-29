import sys
import signal
import xbox
import RPi.GPIO as GPIO

# Print with colors in terminal
class bcolors:
    RIGHT = '\033[95m'
    LEFT = '\033[94m'
    GAS = '\033[92m'
    WARNING = '\033[93m'
    BREAK = '\033[91m'
    ENDC = '\033[0m'

# Format floating point number to string format -x.xxx
def fmtFloat(n):
	return '{:6.3}'.format(n)

# handle ctrl + c interrupt
def exit_program(signum, frame):
	if joy:
		joy.close()
	sys.exit(0)

signal.signal(signal.SIGINT, exit_program)

# RPi.GPIO options
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Setup pin 10 as a simulated break / backward
# Params:
#	- Frequency : 100 hz
#	- Duty Cycle : 0 %
GPIO.setup(10, GPIO.OUT)
brk = GPIO.PWM(10, 100)
brk.start(0)

# Setup pin 21 as a simulated gas / forward
# Params:
#	- Frequency : 100 hz
#	- Duty Cycle : 0 %
GPIO.setup(21, GPIO.OUT)
gas = GPIO.PWM(21, 100)
gas.start(0)

# Setup pin 9 as a simulated left steering
# Params:
#	- Frequency : 100 hz
#	- Duty Cycle : 0 %
GPIO.setup(12, GPIO.OUT)
leftSteering = GPIO.PWM(12, 100)
leftSteering.start(0)

# Setup pin 8 as a simulated left steering
# Params:
#	- Frequency : 100 hz
#	- Duty Cycle : 0 %
GPIO.setup(8, GPIO.OUT)
rightSteering = GPIO.PWM(8, 100)
rightSteering.start(0)

print "Press a button to connect your device"
joy = xbox.Joystick()
lastLeftAnalogX = 0.0
lastRightTrigger = 0.0
lastLeftTrigger = 0.0
newCycle = 0.0

# Get events until Xbox360 wireless 
while not joy.Back():
# Left analog stick
	if joy.leftX() != lastLeftAnalogX:
		if joy.leftX() < 0.0:
			newCycle = (abs(joy.leftX()) / 1.0) * 100.0
			leftSteering.ChangeDutyCycle(newCycle)
			print bcolors.LEFT + 'Steering left {0:>3} {1:>8} : {2} {3}'.format(':', fmtFloat(joy.leftX()), 'PWM : ', newCycle) + bcolors.ENDC
		else:
			newCycle = (joy.leftX() / 1.0) * 100.0
			rightSteering.ChangeDutyCycle(newCycle)
			print bcolors.RIGHT + 'Steering right {0:>2} {1:>8} : {2} {3}'.format(':', fmtFloat(joy.leftX()), 'PWM : ', newCycle) + bcolors.ENDC
		lastLeftAnalogX = joy.leftX()
	if lastRightTrigger != joy.rightTrigger():
		# DutyCycle calculation
		newCycle = (joy.rightTrigger() / 1.0) * 100.0
		gas.ChangeDutyCycle(newCycle)
		print bcolors.GAS + 'Gas {0:>13} {1:>8} : {2} {3}'.format(':', fmtFloat(joy.rightTrigger()), 'PWM : ', newCycle) + bcolors.ENDC
		lastRightTrigger = joy.rightTrigger()
	if lastLeftTrigger != joy.leftTrigger():
		newCycle = (joy.leftTrigger() / 1.0) * 100.0
		brk.ChangeDutyCycle(newCycle)
		print bcolors.BREAK + 'Break {0:>11} {1:>8} : {2} {3}'.format(':', fmtFloat(joy.leftTrigger()), 'PWM : ', newCycle) + bcolors.ENDC
		lastLeftTrigger = joy.leftTrigger()
	if joy.A():
		print "Horn!"
	if joy.X():
		print "Light!"
joy.close()

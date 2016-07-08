from robotapi import *

PI = 3.141592653589793238462643383279

LEFT_MOTOR = M2
RIGHT_MOTOR = M1
ULTRASONIC_MOTOR = M3
LINE_TRACKER = S1
VICTIM_TRACKER = S2
ULTRASONIC = S3

# Inches
WHEEL_RADIUS = 1
ROBOT_RADIUS = 2.8
ROBOT_LENGTH = 6

ENCODER_KP = 1
ENCODER_KI = 0
ENCODER_KD = 0

LINE_TRACKER_KP = 0
LINE_TRACKER_KI = 0
LINE_TRACKER_KD = 0

ULTRASONIC_KP = 0

LINE_TRACKER_RED = -1
LINE_TRACKER_WHITE = -1
LINE_TRACKER_BLACK = -1

WALL_HUGGING_DISTANCE = 5

# Status variables
lineTrackingComplete = false
numVictimsFound = 0

# Track the victims
def trackVictims():
	count = 0
	while (not lineTrackingComplete):
		curColor = HC.get_colornum()
		# Dark blue
		if (curColor == 2 or curColor == 3):
			PSM.led(1, 255, 0, 0)
            sleep(3)
            PSM.led(1, 0, 0, 0)
            sleep(2)
        else:
        	sleep(0.1)
    numVictimsFound = count

# Follow a line
def followLine(speed, lineColor, backgroundColor, stopCondition, *stopConditionArguments):
	lightPID = PID((lineColor + backgroundColor) / 2, LINE_TRACKER_KP, LINE_TRACKER_KI, LINE_TRACKER_KD)
	while (not stopCondition(*stopConditionArguments)):
		turningAmount = lightPID.update(LINE_TRACKER.colorSensorNXT())
		LEFT_MOTOR.setSpeed(-speed + turningAmount)
		RIGHT_MOTOR.setSpeed(-speed - turningAmount)

	LEFT_MOTOR.brake()
	RIGHT_MOTOR.brake()
	lineTrackingComplete = True

# Set the position of the ultrasonic sensor
def setUltrasonicPosition(degs):
	ultrasonicPID = PID(-degs, ULTRASONIC_KP, 0, 0)
	while (ULTRASONIC_MOTOR.pos() != -degs):
		ultrasonicPID.setSpeed(ultrasonicPID.update(ULTRASONIC_MOTOR.pos()))
	ULTRASONIC_MOTOR.brake()

# Turn the robot by a certain number of degrees
def turnRobot(deg, speed, clockwise):
	LEFT_MOTOR.resetPos()
	RIGHT_MOTOR.resetPos()
	
	speed = abs(speed)
	deg = abs(deg)

	leftSign = 1
	rightSign = -1
	if clockwise:
		leftSign = -1
		rightSign = 1

	robotCircumference = 2 * PI * ROBOT_RADIUS
	wheelCircumference = 2 * PI * WHEEL_RADIUS

	encoderTarget = deg * robotCircumference / wheelCircumference

	rightWheelPID = PID(0, ENCODER_KP, ENCODER_KI, ENCODER_KD)
	print("Target", encoderTarget)

	# PID for the encoder value of the right wheel done with respect to the encoder value of the left wheel
	while (abs(LEFT_MOTOR.pos()) < encoderTarget or abs(RIGHT_MOTOR.pos()) < encoderTarget):
		LEFT_MOTOR.setSpeed(leftSign * speed)
		RIGHT_MOTOR.setSpeed(rightSign * speed + rightWheelPID.update(LEFT_MOTOR.pos() * leftSign / rightSign - RIGHT_MOTOR.pos()))
		print(LEFT_MOTOR.pos())

	LEFT_MOTOR.brake()
	RIGHT_MOTOR.brake()

# Move the robot a certain number of inches forwards or backwards
def moveRobot(distance, speed, forwards):
	LEFT_MOTOR.resetPos()
	RIGHT_MOTOR.resetPos()

	speed = abs(speed)
	distance = abs(distance)

	leftSign = 1
	rightSign = 1
	if forwards:
		leftSign = -1
		rightSign = -1

	wheelCircumference = 2 * PI * WHEEL_RADIUS
	encoderTarget = 360 * distance / wheelCircumference

	rightWheelPID = PID(0, ENCODER_KP, ENCODER_KI, ENCODER_KD)
	
	# PID for the encoder value of the right wheel done with respect to the encoder value of the left wheel
	while (abs(LEFT_MOTOR.pos()) < encoderTarget or abs(RIGHT_MOTOR.pos()) < encoderTarget):
		LEFT_MOTOR.setSpeed(leftSign * speed)
		RIGHT_MOTOR.setSpeed(rightSign * speed + rightWheelPID.update(LEFT_MOTOR.pos() * leftSign / rightSign - RIGHT_MOTOR.pos()))
		print(RIGHT_MOTOR.pos(), LEFT_MOTOR.pos())

	LEFT_MOTOR.brake()
	RIGHT_MOTOR.brake()

def isAboveLine(color, threshold):
	if (LINE_TRACKER.colorSensorNXT() > color - threshold and LINE_TRACKER.colorSensorNXT() < color + threshold):
		return True
	else:
		return False

def readUltrasonicValueAt(degs):
	setUltrasonicPosition(degs)
	return ULTRASONIC.distanceUSEV3in()

def hugRightWall(speed):
	# If you can turn right, turn right
	# Else if there is a wall on the right and a wall in front turn left
	# Else if there is a wall on the right and nothing in front go forward
	
	# Estimated distance left in front of the robot to the wall
	distanceInFront = readUltrasonicValueAt(0)

	# False means left turn, True means right turn
	previousTurn = False
	while (True):		
		if (readUltrasonicValueAt(90) > WALL_HUGGING_DISTANCE + 1):
			if (previousTurn == False):
				moveRobot(ROBOT_LENGTH, speed, True)

			turnRobot(90, speed, True)
			moveRobot(max(0, min(ROBOT_LENGTH, readUltrasonicValueAt(0) - WALL_HUGGING_DISTANCE)), speed, True)
			distanceInFront = readUltrasonicValueAt(0)
			previousTurn = True
		else if (distanceInFront < WALL_HUGGING_DISTANCE + 1 and readUltrasonicValueAt(0) < WALL_HUGGING_DISTANCE):
			turnRobot(90, speed, False)
			distanceInFront = readUltrasonicValueAt(0)
			previousTurn = False
		else:
			moveRobot(1, speed, True)
			distanceInFront -= 1

def main():
	# Init
	#VICTIM_TRACKER.activateCustomSensorI2C()
	
	# Line following and victim tracking
	#victimThread = Thread(target = trackVictims)
	#victimThread.start()
	#followLine(30, LINE_TRACKER_WHITE, LINE_TRACKER_BLACK, isAboveLine, LINE_TRACKER_RED, 30)

	# Traversing the house by following the right wall 	
	moveRobot(10, 40, True)	

if __name__ == "__main__":
	main()
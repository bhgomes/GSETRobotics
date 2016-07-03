from robotapi import *

PI = 3.141592653589793238462643383279

LEFT_MOTOR = M2
RIGHT_MOTOR = M1
LINE_TRACKER = S1
VICTIM_TRACKER = S2
ULTRASONIC = S3

# Inches
WHEEL_RADIUS = 1
ROBOT_RADIUS = 2.8

ENCODER_KP = 1
ENCODER_KI = 0
ENCODER_KD = 0

LINE_TRACKER_KP = 0
LINE_TRACKER_KI = 0
LINE_TRACKER_KD = 0

LINE_TRACKER_RED = -1
LINE_TRACKER_WHITE = -1
LINE_TRACKER_BLACK = -1

# Follow a line
def followLine(speed, lineColor, backgroundColor, stopCondition) {
	lightPID = PID((lineColor + backgroundColor) / 2, LINE_TRACKER_KP, LINE_TRACKER_KI, LINE_TRACKER_KD)
	while (not stopCondition()):
		turningAmount = lightPID.update(LINE_TRACKER.colorSensorNXT())
		LEFT_MOTOR.setSpeed(-speed + turningAmount)
		RIGHT_MOTOR.setSpeed(-speed - turningAmount)

	LEFT_MOTOR.brake()
	RIGHT_MOTOR.brake()
}

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

def main():
	# Line following and victim tracking
	
	# Traversing the house
	moveRobot(5, 30, False)

if __name__ == "__main__":
	main()
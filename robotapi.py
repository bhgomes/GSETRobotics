# ROBOT API for GSET Robotics Competition
# by bhgomes

from PiStorms import PiStorms

from functools import wraps
from time import sleep

import sys

PSM = PiStorms()

SCREEN = PSM.screen

M1 = PSM.BAM1
M2 = PSM.BAM2
AM = (M1, M2)

M3 = PSM.BBM1
M4 = PSM.BBM2
BM = (M3, M4)

ML = AM + BM

S1 = PSM.BAS1
S2 = PSM.BAS2
AS = (S1, S2)

S3 = PSM.BBS1
S4 = PSM.BBS2
BS = (S3, S4)

SL = AS + BS

BA = (AM, AS)
BB = (BM, BS)

GO   = PSM.isKeyPressed
STOP = PSM.isKeyPressed

# CONTROL STRUCTURES #

def whileloop(condition, exit_function, *ars, **kwars):
    ''' '''
    def whileloop_decorator(function):
        ''' '''
        @wraps(function)
        def __looping(*args, **kwargs):
            ''' '''
            while True:
                function(*args, **kwargs)
                if condition:
                    exit_function(*ars, **kwars)
                    break
        return __looping
    return whileloop_decorator

def repeat(n):
    ''' '''
    def repeat_decorator(function):
        ''' '''
        @wraps(function)
        def __looping(*args, **kwargs):
            ''' '''
            for _ in range(n):
                function(*args, **kwargs)
        return __looping
    return repeat_decorator

def irepeat(start, end):
    ''' '''
    def irepeat_decorator(function):
        ''' '''
        @wraps(function)
        def __looping(*args, **kwargs):
            ''' '''
            for i in range(start, end):
                function(i, *args, **kwargs)
        return __looping
    return irepeat_decorator

def sleeper(dt):
    def sleeper_decorator(function):
        @wraps(function)
        def __sleeper(*args, **kwargs):
            return
        return __sleeper
    return sleeper_decorator

# END CONTROL STRUCTURES #

# ACTIONS #

def syncprint(msg):
    SCREEN.termPrintln(msg)
    print(msg)

def neutral_exit(msg):
    ''' NEUTRAL EXIT does not care about the motor '''
    SCREEN.clearScreen()
    syncprint("\n" + msg)
    PSM.led(1, 0, 0, 0)
    sleep(0.5)

def safe_exit(msg):
    ''' SAFE EXIT floats the engine '''
    AM[0].floatSync()
    BM[0].floatSync()
    neutral_exit(msg)

def unsafe_exit(msg):
    ''' UNSAFE EXIT brakes the engine '''
    AM[0].brakeSync()
    BM[0].brakeSync()
    neutral_exit(msg)

# not optimized for synchronous motors
def set_motor_speed(**motors):
    ''' SET MOTOR SPEED sets the speed of any motor or motors '''
    for motor, speed in motors.items():
        motor.setSpeed(speed)

# END ACTIONS #

# TESTS #

def rotation_test(left, right, speed=50, parallel=True):
    ''' ROTATION TEST spins the robot at a default of 50 power '''
    set_motor_speed(left=speed, right=(-speed if parallel else speed))

@whileloop(STOP, safe_exit, "Exiting Tests")
@sleeper(0.25)
def tests():
    ''' TESTS is a testing suite for the robotapi '''
    rotation_test(M1, M2)

# END TESTS #

# MAIN #

if __name__ == "__main__":
    ''' MAIN runs tests and calibrates the robot '''
    ARGV = sys.argv
    ARGL = len(ARGV)

    syncprint("< PiStorms Robotic System >")

    if ARGL == 1:
        syncprint("running tests: ")
    elif ARGL == 2:
        pass
    elif ARGL == 3:
        pass
    elif ARGL == 4:
        pass
    else:
        pass

# END MAIN #

# ROBOT API for GSET Robotics Competition
# robotapi.py
# by bhgomes

import sys
import time
import getopt

from functools import wraps
import numpy as np
from time import sleep
from threading import Thread

from PiStorms import PiStorms
from mindsensors_i2c import mindsensors_i2c

################################################################################
############################# ABSTRACT STRUCTURES ##############################
################################################################################

# CLASSES #

class PID(object):
    def __init__(self, setpoint, Kp, Ki, Kd):
        self.setpoint   = setpoint
        self.Kp         = Kp
        self.Ki         = Ki
        self.Kd         = Kd
        self.last_time  = 0
        self.last_error = 0
        self.output     = 0
        self.pterm      = 0
        self.iterm      = 0
        self.dterm      = 0

    def error(self, feedback):
        return self.setpoint - feedback

    def update(self, feedback):
        tim = time.time()
        err = self.error(feedback)

        dt = tim - self.last_time
        de = err - self.last_error

        self.last_time  = tim
        self.last_error = err

        self.pterm  = err
        self.iterm += err * dt
        self.dterm  = de  / dt

        self.output = (self.Kp * self.pterm) + (self.Ki * self.iterm) - (self.Kd * self.dterm)

        return self.output

class AreaMap(object):
    def __init__(self):
        pass

    def __call__(self):
        pass

class Scanner(object):
    def __init__(self, amap):
        self.amap = amap

    def __call__(self):
        pass

# END CLASSES #

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
                if condition(*args, **kwargs):
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

def timer(t, dt):
    ''' '''
    def timer_decorator(function):
        ''' '''
        @wraps(function)
        def __timer(*args, **kwargs):
            ''' '''
            b = t()
            v = function(*args, **kwargs)
            return ((t() - b) * dt, v)
        return __timer
    return timer_decorator

def threadable(function):
    @wraps(funcion)
    def __threadable(*args, **kwargs):
        return Thread(target=function)
    return __threadable

def sleeper(dt):
    ''' '''
    def sleeper_decorator(function):
        ''' '''
        @wraps(function)
        def __sleeper(*args, **kwargs):
            ''' '''
            return
        return __sleeper
    return sleeper_decorator

# END CONTROL STRUCTURES #

################################################################################
############################# PISTORMS STRUCTURES ##############################
################################################################################

# CLASSES #

class HiTechnicColorV2(mindsensors_i2c):
    Color_ADDRESS = (0x02)
    Color_COMMAND = (0x41)

    def __init__(self, color_address = Color_ADDRESS):
        mindsensors_i2c.__init__(self, color_address >> 1)

    def get_colornum(self):
        try:
            return (self.readIntegerBE(self.Color_COMMAND))
        except:
            print("Error: Could not read color")
            return ""

HC = HiTechnicColorV2()

# END CLASSES #

# CONSTANTS #

PSM = PiStorms()

SCREEN = PSM.screen

M1   = PSM.BAM1
M2   = PSM.BAM2
AM   = (M1, M2)

M3   = PSM.BBM1
M4   = PSM.BBM2
BM   = (M3, M4)

ML   = AM + BM

S1   = PSM.BAS1
S2   = PSM.BAS2
AS   = (S1, S2)

S3   = PSM.BBS1
S4   = PSM.BBS2
BS   = (S3, S4)

SL   = AS + BS

BA   = (AM, AS)
BB   = (BM, BS)

GO   = PSM.isKeyPressed
STOP = PSM.isKeyPressed

# END CONSTANTS #

# ACTIONS #

def syncprint(msg):
    SCREEN.termPrintln(msg)
    print(msg)

def neutral_exit(msg):
    ''' NEUTRAL EXIT does not care about the motor '''
    SCREEN.clearScreen()
    syncprint(msg)
    PSM.led(1, 0, 0, 0)
    sleep(0.5)
    SCREEN.refresh()

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

def test_sensor_value():
    syncprint(S3.lightSensorNXT(True))

def rotation_test(left, right, speed=50, parallel=True):
    ''' ROTATION TEST spins the robot at a default of 50 power '''
    set_motor_speed(left=speed, right=(-speed if parallel else speed))

@whileloop(STOP(), safe_exit, "Exiting Tests")
@sleeper(0.25)
def tests():
    ''' TESTS is a testing suite for the robotapi '''
    rotation_test(M1, M2)

# END TESTS #

# MAIN #

def main():
    ''' MAIN runs tests and calibrates the robot '''

    """
    try:
        opts, args = getopt.getopt(args, "a:b:c:defg",
                                   ["a=", "b=", "c=",
                                    "d", "e", "f", "g"])
    except getopt.error, err:
        print err
        print "use -h/--help for command line help"
        return 2

    for o, a in opts:
        if o in (,):

        if o in (,):

        if o in (,):

        if o in (,):

        if o in ("-h", "--help"):
            print (__doc__)
            return 0
    """

    syncprint("< PiStorms Robotic System >")

    safe_exit("Exit")

if __name__ == "__main__":
    sys.exit(main())

# END MAIN #

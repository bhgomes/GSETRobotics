# ROBOT API for GSET Robotics Competition
# by bhgomes

from PiStorms import PiStorms
from time import sleep

psm = PiStorms()

SCREEN = psm.screen

M1 = psm.BAM1
M2 = psm.BAM2
AM = (M1, M2)

M3 = psm.BBM1
M4 = psm.BBM2
BM = (M3, M4)

ML = AM + BM

S1 = psm.BAS1
S2 = psm.BAS2
AS = (S1, S2)

S3 = psm.BBS1
S4 = psm.BBS2
BS = (S3, S4)

SL = AS + BS

BA = (AM, AS)
BB = (BM, BS)

GO   = psm.isKeyPressed
STOP = psm.isKeyPressed

# CONTROL STRUCTURES #

def whileloop(condition, exit_function, *ars, **kwars):
    def inner_decorator(function):
        def looping(*args, **kwargs):
            while True:
                function(*args, **kwargs)
                if condition:
                    exit_function(*ars, **kwars)
                    break
        return looping
    return inner_decorator

# END CONTROL STRUCTURES #

def safe_exit(msg):
    AM[0].brakeSync()
    BM[0].brakeSync()
    SCREEN.clearScreen()
    SCREEN.termPrintln("\n" + msg)
    psm.led(1,0,0,0)
    sleep(0.5)

# TESTS #

def rotation_test(speed):
    M1.setSpeed(speed)
    M2.setSpeed(-speed)

@whileloop(STOP, safe_exit, "Exiting Tests")
def tests():
    rotation_test(50)

# END TESTS #

# ACTIONS #

# END ACTIONS #
from naoqi import ALProxy
from time import sleep

robotIP = "localhost"
robotPort = 9559

motion = ALProxy("ALMotion", robotIP, robotPort)
leds = ALProxy("ALLeds", robotIP, robotPort)

MIN_SHOULDER_PITCH = -2.086
MAX_SHOULDER_PITCH = -1.178
leftArmJoints = ['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll']

# Loosen the left arm
motion.setStiffnesses(leftArmJoints, 0.0)

def main():
    while True:
        # Read the current shoulder pitch position
        leftArmAngles = motion.getAngles('LShoulderPitch', True)

        # If the value indicates the arm is pointing upright
        if (leftArmAngles[0] > MIN_SHOULDER_PITCH) \
            and (leftArmAngles[0] < MAX_SHOULDER_PITCH):
            break

        # Prevent reading too often.
        sleep(0.25)
    
    # Turn on the face LED's as green for five seconds.
    print "Setting LEDs on"
    leds.fadeRGB("FaceLeds", 0x00FF00, 1)
    sleep(5)
    print "Setting LEDS off"
    leds.fadeRGB("FaceLeds", 0x000000, 0)

    # Repeat the main loop
    main()

main()
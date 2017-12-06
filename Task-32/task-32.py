from naoqi import ALProxy
from time import sleep

robotIP = "localhost"
robotPort = 9559

motion = ALProxy("ALMotion", robotIP, robotPort)
leds = ALProxy("ALLeds", robotIP, robotPort)
tts = ALProxy("ALTextToSpeech", robotIP, robotPort)

MIN_SHOULDER_PITCH = -2.086
MAX_SHOULDER_PITCH = -1.178
leftArmJoints = ['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll']

CurrentlyOn = False

# Loosen the left arm
motion.setStiffnesses(leftArmJoints, 0.0)

# Disable face LED's
leds.fadeRGB("FaceLeds", 0x000000, 0)

tts.say("I am ready. Gently move my left arm.")

while True:
    # Read the current shoulder pitch position
    leftArmAngles = motion.getAngles('LShoulderPitch', True)

    # If the value indicates the arm is pointing upright
    if (leftArmAngles[0] > MIN_SHOULDER_PITCH) \
        and (leftArmAngles[0] < MAX_SHOULDER_PITCH):
        if not CurrentlyOn:
            print "Setting LEDs on"
            leds.fadeRGB("FaceLeds", 0x00FF00, 0)
            CurrentlyOn = True
    else:
        if CurrentlyOn:
            print "Setting LEDS off"
            leds.fadeRGB("FaceLeds", 0x000000, 0)
            CurrentlyOn = False

    # Prevent reading too often.
    sleep(0.25)
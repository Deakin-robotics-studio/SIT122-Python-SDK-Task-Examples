from naoqi import ALProxy
from time import sleep
import math, threading

robotIP = "localhost"
robotPort = 9559

posture = ALProxy("ALRobotPosture", robotIP, robotPort)
motion = ALProxy("ALMotion", robotIP, robotPort)
tts = ALProxy("ALTextToSpeech", robotIP, robotPort)

# Create a function that will make the robot speak.
def makeRobotSpeak(tts, direction):

    sleep(3.0)
    print "I am currently walking %s" % (direction)
    tts.say("I am currently walking %s" % (direction))

# Ensure the robot is sitting first.
posture.goToPosture("Stand", 1.0)

# Walk four sides of a rectangle.
directions = ["East", "North", "West", "South"]

for i in range(0,4):

    # Begin robot speech thread.
    robotSpeechThread = threading.Thread(target=makeRobotSpeak, args=(tts,directions[i]))
    robotSpeechThread.start()

    # Walk forwards one metre.
    motion.moveTo(1, 0, 0)

    # Turn 90 degrees.
    motion.moveTo(0, 0, (math.pi / 2))

    # Ensure the robot speech thread has finished.
    robotSpeechThread.join()

# Go to sit again.
posture.goToPosture("Sit", 1.0)
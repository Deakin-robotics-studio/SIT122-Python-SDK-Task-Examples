from naoqi import ALProxy
from time import sleep
import math

posture = ALProxy("ALRobotPosture", "localhost", 9559)
motion = ALProxy("ALMotion", "localhost", 9559)

# Ensure the robot is standing up.
posture.goToPosture("Stand", 1.0)

# Walk forwards 50 centremetres at normal speed
motion.moveTo(0.5, 0, 0)
sleep(5)

# Slow but stable movement.
motion.moveTo(0.5, 0, 0, [
    ['MaxStepX', 0.06],
    ['MaxStepY', 0.11],
    ['MaxStepTheta', 0.15],
    ['MaxStepFrequency', 0.2]
])

posture.goToPosture("Sit", 1.0)
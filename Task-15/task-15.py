from naoqi import ALProxy
from time import sleep
import math

posture = ALProxy("ALRobotPosture", "localhost", 9559)
motion = ALProxy("ALMotion", "localhost", 9559)

# Stables walking parameters for walking a curved path
stable = [
    ['MaxStepX', 0.06],
    ['MaxStepY', 0.11],
    ['MaxStepTheta', 0.15],
    ['MaxStepFrequency', 0.2]
]

# Ensure the robot is standing up.
posture.goToPosture("Stand", 1.0)

# Move to the first quarter side of the circle
motion.moveTo(0.5, 0.5, (math.pi / 2), stable)
sleep(1)

# Move to the second quarter side of the circle
motion.moveTo(0.5, 0.5, (math.pi / 2), stable)
sleep(1)

# Move to the third quarter side of the circle
motion.moveTo(0.5, 0.5, (math.pi / 2), stable)
sleep(1)

# Move to the starting point of the circle
motion.moveTo(0.5, 0.5, (math.pi / 2), stable)
sleep(1)

posture.goToPosture("Sit", 1.0)
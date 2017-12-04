from naoqi import ALProxy
from time import sleep
import math

posture = ALProxy("ALRobotPosture", "localhost", 9559)
motion = ALProxy("ALMotion", "localhost", 9559)

# Ensure the robot is standing up.
posture.goToPosture("Stand", 1.0)

# Slow but stable movement.
motion.moveTo(1, 0, 0, [
    ['MaxStepX', 0.06],
    ['MaxStepY', 0.11],
    ['MaxStepTheta', 0.15],
    ['MaxStepFrequency', 0.2]
])
sleep(1)

# Faster but less stable movement.
motion.moveTo(1, 0, 0, [
    ['MaxStepX', 0.2],
    ['MaxStepY', 0.2],
    ['MaxStepTheta', 0.2],
    ['MaxStepFrequency', 0.5]
])
sleep(1)

# Large side steps, faster
motion.moveTo(0, 1, 0, [
    ['MaxStepY', 0.5],
    ['MaxStepFrequency', 0.5]
])
sleep(1)

# Small side steps, flower
motion.moveTo(0, 1, 0, [
    ['MaxStepY', 0.2],
    ['MaxStepFrequency', 0.2]
])
sleep(1)

# Turn 180 degrees, less-stable
motion.moveTo(0, 0, math.pi, [
    ['MaxStepTheta', 0.2]
])
sleep(1)

# Turn 180 degrees, more-stable
motion.moveTo(0, 0, math.pi)
sleep(1)

posture.goToPosture("Sit", 1.0)
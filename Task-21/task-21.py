from naoqi import ALProxy
from time import sleep

posture = ALProxy("ALRobotPosture", "localhost", 9559)
motion = ALProxy("ALMotion", "localhost", 9559)

# Store the left arm joins in an array.
leftArmJoints = ['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll']

# Ensure the robot is sitting first.
posture.goToPosture("Sit", 1.0)

# Get the original position.
originLeftArmPosition = motion.getAngles(leftArmJoints, True)

# Set the stiffness.
motion.setStiffnesses(leftArmJoints, 1.0)

# Move arm upright.
motion.angleInterpolation(["LShoulderPitch", "LShoulderRoll"], [-1.2506, 0.281058], [2, 2], True)

sleep(5)

# Move arm back.
motion.angleInterpolation(leftArmJoints, originLeftArmPosition, [2, 2, 2, 2], True)

# Relax the arm.
motion.setStiffnesses(leftArmJoints, 0.0)

# Go to sit again
posture.goToPosture("Sit", 1.0)
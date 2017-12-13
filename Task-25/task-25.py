from naoqi import ALProxy
from time import sleep
import threading

posture = ALProxy("ALRobotPosture", "localhost", 9559)
motion = ALProxy("ALMotion", "localhost", 9559)

# Create a function that will make the robot move its head
def makeRobotWave(motion):
    print "makeRobotWave thread starting. Sleeping for 2.0 seconds."
    sleep(2.0)
    print "Make robot wave!"

    # Choregraphe bezier export in Python.
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([2, 3, 5, 6])
    keys.append([[-0.17, [3, -0.666667, 0], [3, 0.333333, 0]], [-0.17, [3, -0.333333, 0], [3, 0.666667, 0]], [-0.17, [3, -0.666667, 0], [3, 0.333333, 0]], [-0.17, [3, -0.333333, 0], [3, 0, 0]]])

    names.append("HeadYaw")
    times.append([2, 3, 5, 6, 8])
    keys.append([[-1.48377, [3, -0.666667, 0], [3, 0.333333, 0]], [-1.48377, [3, -0.333333, 0], [3, 0.666667, 0]], [1.62839, [3, -0.666667, 0], [3, 0.333333, 0]], [1.62839, [3, -0.333333, 0], [3, 0.666667, 0]], [0, [3, -0.666667, 0], [3, 0, 0]]])

    motion.angleInterpolationBezier(names, times, keys)


    print "makeRobotWave finished"

# Ensure the robot is sitting first.
posture.goToPosture("Stand", 1.0)

# Create the robot waving thread.
robotWaveThread = threading.Thread(target=makeRobotWave, args=(motion,))

# Start the threads execution and continue executing the rest of the program separately.
robotWaveThread.start()

# Walk forwards one meter.
motion.moveTo(1, 0, 0)

# Wait for the robotWaveThread to finish executing before trying to sit down.
# This prevents the robot sitting and waving at the same time, which we don't want.
robotWaveThread.join()

# Go to sit again.
posture.goToPosture("Sit", 1.0)
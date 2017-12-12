from naoqi import ALProxy
posture = ALProxy("ALRobotPosture", "localhost", 9559)
motion = ALProxy("ALMotion", "localhost", 9559)

motion.moveTo(1, 1, 0)

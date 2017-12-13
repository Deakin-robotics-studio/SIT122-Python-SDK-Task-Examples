from naoqi import ALProxy
import math, random, time

robotIP = "localhost"
robotPort = 9559

MIN_SONAR_THRESHHOLD = 0.5
MAX_TRIGGER_COUNT = 3
MAX_RUNTIME_SECONDS = 120

stable = [
    ['MaxStepX', 0.09],
    ['MaxStepY', 0.09],
    ['MaxStepTheta', 0.09],
    ['MaxStepFrequency', 0.15]
]

class SenseReasonReact():
    def __init__(self, robotIP, robotPort):

        # Start time
        self.startTime = time.time()
        self.quit = False

        # Link with posture and motion
        self.posture = ALProxy("ALRobotPosture", robotIP, robotPort)
        self.motion = ALProxy("ALMotion", robotIP, robotPort)
        self.tts = ALProxy("ALTextToSpeech", robotIP, robotPort)

        # Setup sonar
        self.sonar = ALProxy("ALSonar", robotIP, robotPort)
        self.sonar.subscribe("SenseReasonReact")

        # Register with memory
        self.memory = ALProxy("ALMemory", robotIP, robotPort)

        self.leftSonarVal = 5
        self.rightSonarVal = 5
        self.objectTriggerCount = 0
        self.objectDetected = False

        self.onStart()
        self.mainLoop()
    
    def onStart(self):
        self.posture.goToPosture('Stand', 1)

    def onEnd(self):
        self.posture.goToPosture('Sit', 1)

    def senseObjects(self):
        self.leftSonarVal = self.memory.getData("Device/SubDeviceList/US/Left/Sensor/Value")
        self.rightSonarVal = self.memory.getData("Device/SubDeviceList/US/Right/Sensor/Value")

    def reasonData(self):
        # Determine if there is an object in the way.
        if self.leftSonarVal < MIN_SONAR_THRESHHOLD or self.rightSonarVal < MIN_SONAR_THRESHHOLD:
            self.objectTriggerCount += 1

            # Only trigger the object detection if this has happened more than MAX_TRIGGER_COUNT 
            # times in a row. 
            if ( self.objectTriggerCount > MAX_TRIGGER_COUNT ):
                self.objectTriggerCount = 0
                self.objectDetected = True
        else:
            self.objectTriggerCount = 0
            self.objectDetected = False
        
        # How long has the program been running?
        if ( time.time() - self.startTime ) >= MAX_RUNTIME_SECONDS:
            self.quit = True

    def act(self):

        if self.quit:
            self.tts.post.say("I am getting tired. Goodbye.")
            self.motion.stopMove()
            self.onEnd()
        
        if self.objectDetected:
            self.tts.post.say("Ah, there is an object in my way.")
            self.motion.stopMove()
            time.sleep(1)

            self.objectDetected = False

            # Turn 180 degrees.
            self.motion.moveTo(0, 0, (math.pi) / 2, stable)
            
            # Start walking again.
            self.motion.post.moveTo(1, 0, 0, stable)
        
        else:
            if not self.motion.moveIsActive():
                # Face random direction
                self.motion.moveTo(0, 0, random.uniform(0.0, (2 * math.pi) + 1), stable)
                time.sleep(1)

                # Walk forwards again.
                self.motion.post.moveTo(1, 0, 0, stable)


    def mainLoop(self):

        # Sense
        self.senseObjects()

        # Reason
        self.reasonData()

        # Act
        self.act()

        time.sleep(0.1)

        # Continue calling.
        if not self.quit:
            self.mainLoop()

Main = SenseReasonReact(robotIP, robotPort)
from naoqi import ALProxy, ALBroker, ALModule
from time import sleep
import math

robotIP = "localhost"
robotPort = 9559

NAO_MARK_QUIT = 64
NAO_MARK_STAND = 80
NAO_MARK_SIT = 84
NAO_MARK_WALK_FORWARD = 85
NAO_MARK_TURN_LEFT = 107
NAO_MARK_TURN_RIGHT = 108

stable = [
    ['MaxStepX', 0.09],
    ['MaxStepY', 0.09],
    ['MaxStepTheta', 0.09],
    ['MaxStepFrequency', 0.15]
]

class NaoMarkNavigator(ALModule):
    
    def __init__(self, name):
        self.quit = False
        self.detectLock = False
        self.standing = False

        # Register our module with NAOqi
        ALModule.__init__(self, name)

        self.motion = ALProxy("ALMotion")
        self.posture = ALProxy("ALRobotPosture")
        self.tts = ALProxy("ALTextToSpeech")

        # Register landmark detection module
        self.memory = ALProxy("ALMemory") 
        self.ld = ALProxy("ALLandMarkDetection")
        self.ld.subscribe("NaoMarkNavigator")

        # Subscribe the "onFaceDetected" function to "FaceDetected".
        self.memory.subscribeToEvent("LandmarkDetected",
            "NaoMarkNavigator",
            "onMarkDetected")

        self.tts.say("Show me NAOMarks to control my movement.")

        # Start detections.
        self.startDetection()

    def startDetection(self):
        self.detectLock = False
    
    def endDetection(self):
        self.detectLock = True

    # Sensing
    def onMarkDetected(self, eventName, eventData):

        if self.detectLock:
            return
        
        # Pause detection to prevent multiple events being fired.
        self.endDetection()

        # Ensure the data supplied to this event callback is correct.
        if len(eventData) < 4:
            return

        # See http://doc.aldebaran.com/1-14/naoqi/vision/allandmarkdetection-api.html#LandmarkDetected
        # for LandMarkDetected value structure (including position in real world data)/
        naoMarkNumber = eventData[1][0][1][0]
        foundOnCamera = eventData[4]

        self.reason(naoMarkNumber, foundOnCamera)
        
        # Restart the detection.
        sleep(1.0)
        self.startDetection()

    # Reasoning / Acting
    def reason(self, naoMarkNumber, camera):

        if naoMarkNumber == NAO_MARK_QUIT:
            self.quit = True
        elif naoMarkNumber == NAO_MARK_STAND:
            self.onStandUp()
        elif naoMarkNumber == NAO_MARK_SIT:
            self.onSitDown()
        elif naoMarkNumber == NAO_MARK_WALK_FORWARD:
            self.onWalkForwards()
        elif naoMarkNumber == NAO_MARK_TURN_LEFT:
            self.onTurn('left')
        elif naoMarkNumber == NAO_MARK_TURN_RIGHT:
            self.onTurn('right')

        else:
            # Acting.
            self.tts.say("I see a NAOMark, but I don't know what to do with it.")
        
    def onStandUp(self):
        if not self.standing:
            self.tts.say("Okay. Standing up!")
            self.posture.goToPosture('Stand', 1.0)
            self.standing = True
        else:
            self.tts.say("I am already standing!")

    def onSitDown(self):
        if self.standing:
            self.tts.say("Okay. Sitting down!")
            self.posture.goToPosture('Sit', 1.0)
            self.standing = False
        else:
            self.tts.say("I am already sitting!")
    
    def onWalkForwards(self):
        if not self.standing:
            self.tts.say("I must be standing to walk forwards.")
            return
        
        self.tts.say("Okay. Walking forwards!")
        self.motion.moveTo(0.5, 0, 0, stable)

    def onTurn(self, direction):
        if not self.standing:
            self.tts.say("I must be standing to turn %s." % direction)
            return

        self.tts.say("Okay. Turning %s!" % direction)

        if direction == "left":
            radians = math.pi / 4
        elif direction == "right":
            radians = 0 - math.pi / 4
        
        self.motion.moveTo(0, 0, radians, stable)

    def onEnd(self):
        self.posture.goToPosture('Sit', 1.0)
        self.tts.say("Goodbye.")


def main(ip, port):
    global NaoMarkNavigator

    # Setup the data broker.
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # Bind to socket root
       0,           # Auto-select port
       ip,          # Parent broker IP
       port)        # Parent broker port

    NaoMarkNavigator = NaoMarkNavigator("NaoMarkNavigator")

    try:
        while True:
            # 100 miliseconds is an acceptable amount of input delay time.
            if NaoMarkNavigator.quit == True:
                NaoMarkNavigator.onEnd()
                break
            sleep(0.1)
    except KeyboardInterrupt:
        NaoMarkNavigator.onEnd()
        myBroker.shutdown()
        

main(robotIP, robotPort)
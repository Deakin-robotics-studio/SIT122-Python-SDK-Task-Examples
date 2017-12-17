from naoqi import ALProxy, ALBroker, ALModule
from time import sleep

robotIP = "localhost"
robotPort = 9559
memory = None

EVENTS = ["HandRightBackTouched", "HandLeftBackTouched", "RightBumperPressed", "LeftBumperPressed", "RearTactilTouched"]


class BallTracker(ALModule):

    def __init__(self, name):
        global memory
        self.codeProgression = 0
        self.quit = False

        # Register our module with NAOqi
        ALModule.__init__(self, name)
        memory = ALProxy("ALMemory")
        self.tts = ALProxy("ALTextToSpeech")
        self.motion = ALProxy("ALMotion")

        # Subscribe to the rear tacile sensor touch event.
        memory.subscribeToEvent("RearTactilTouched",
            "BallTracker",
            "onRearTactilTouched")

        # Register speech recognition
        self.asr = ALProxy("ALBallTracker")
        self.asr.setLanguage("English")
        self.asr.setVisualExpression(True)

        # Subscribe to speech detection
        memory.subscribeToEvent("WordRecognized",
            "BallTracker",
            "onWordRecognized")

        # Create the tracker.
        self.redBallTracker = ALProxy("ALRedBallTracker")

        self.startListening()

    def startListening(self):
        self.asr.pause(False)
        self.asr.setVocabulary(['awake'])

    def stopListening(self):
        self.asr.pause(True)

    def onWordRecognized(self, ref, spot):
        # As only one command exists in this program, this will only ever be
        # be called for one command, and therefore, we don't need to check
        # whether its specific or not.
        self.stopListening()
        self.tts.say('Hey')
        self.startBallTracker()

    def onRearTactilTouched(self):
        self.tts.say('Goodbye')
        self.stopBallTracker()
        self.quit = True

    def startBallTracker(self):
        self.motion.setStiffnesses("Head", 1.0)
        self.redBallTracker.startTracker()

    def stopBallTracker(self):
        self.redBallTracker.stopTracker()
        self.motion.setStiffnesses("Head", 0.0)


def main(ip, port):
    global BallTracker

    # Setup the data broker.
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # Bind to socket root
       0,           # Auto-select port
       ip,          # Parent broker IP
       port)        # Parent broker port

    BallTracker = BallTracker("BallTracker")

    try:
        while not BallTracker.quit:
            # 100 miliseconds is an acceptable amount of input delay time.
            sleep(0.1)
    except KeyboardInterrupt:
        myBroker.shutdown()

main(robotIP, robotPort)

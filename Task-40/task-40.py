from naoqi import ALProxy, ALBroker, ALModule
from time import sleep

robotIP = "localhost"
robotPort = 9559

NAO_MARK_QUIT = 119
NAO_MARK_JOKE = 130
REQUIRED_CAMERA = "CameraTop"

class NaoMarkDetector(ALModule):
    
    def __init__(self, name):
        self.quit = False
        self.detectLock = False

        # Register our module with NAOqi
        ALModule.__init__(self, name)
        self.tts = ALProxy("ALTextToSpeech")

        # Register landmark detection module
        self.memory = ALProxy("ALMemory") 
        self.ld = ALProxy("ALLandMarkDetection")
        self.ld.subscribe("NaoMarkDetector")

        # Subscribe the "onFaceDetected" function to "FaceDetected".
        self.memory.subscribeToEvent("LandmarkDetected",
            "NaoMarkDetector",
            "onMarkDetected")

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

    # Reasoning.
    def reason(self, naoMarkNumber, camera):
        if not camera == REQUIRED_CAMERA:
            # Acting.
            self.tts.say("I see a NAOMark, but not with my top camera.")
            return

        if naoMarkNumber == NAO_MARK_QUIT:
            # Acting.
            self.quit = True
        elif naoMarkNumber == NAO_MARK_JOKE:
            # Acting.
            self.tts.say("Sometimes, I dream of flying away in a spaceship.")
        else:
            # Acting.
            self.tts.say("I see a NAOMark. It's number is %s" % str(naoMarkNumber))

    def onEnd(self):
        self.tts.say("Goodbye.")


def main(ip, port):
    global NaoMarkDetector

    # Setup the data broker.
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # Bind to socket root
       0,           # Auto-select port
       ip,          # Parent broker IP
       port)        # Parent broker port

    NaoMarkDetector = NaoMarkDetector("NaoMarkDetector")

    try:
        while True:
            # 100 miliseconds is an acceptable amount of input delay time.
            if NaoMarkDetector.quit == True:
                NaoMarkDetector.onEnd()
                break
            sleep(0.1)
    except KeyboardInterrupt:
        NaoMarkDetector.onEnd()
        myBroker.shutdown()
        

main(robotIP, robotPort)
from naoqi import ALProxy, ALBroker, ALModule
from time import sleep
from random import randint

robotIP = "localhost"
robotPort = 9559

class FaceDetector(ALModule):
    
    def __init__(self, name):
        self.quit = False
        self.detectLock = False
        self.faceCounter = 0

        # Register our module with NAOqi
        ALModule.__init__(self, name)
        self.tts = ALProxy("ALTextToSpeech")

        # Register facial recognition module
        self.memory = ALProxy("ALMemory")    
        self.fr = ALProxy("ALFaceDetection")
        self.fr.subscribe("FaceDetector")

        # Subscribe the "onFaceDetected" function to "FaceDetected".
        self.memory.subscribeToEvent("FaceDetected",
            "FaceDetector",
            "onFaceDetected")

        self.startRecognition()

    def onFaceDetected(self, value):
        # self.detectLock will be True if a face has already been seen.
        # to prevent the Nao doubling up on faces, only continue if self.detectLock is False
        if self.detectLock:
            return
        
        # Pause recognition.
        self.stopRecognition()

        self.faceCounter = self.faceCounter + 1
        self.tts.say("Hello, I see you!")
        sleep(1)

        if self.faceCounter >= 3:
            self.quit = True
            return

        # Restart the recognition.
        self.startRecognition()

    def startRecognition(self):
        self.detectLock = False
        self.fr.setRecognitionEnabled(True)

    def stopRecognition(self):
        self.detectLock = True
        self.fr.setRecognitionEnabled(False)

    def onEnd(self):
        self.stopRecognition()
        self.tts.say("Goodbye.")


def main(ip, port):
    global FaceDetector

    # Setup the data broker.
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # Bind to socket root
       0,           # Auto-select port
       ip,          # Parent broker IP
       port)        # Parent broker port

    FaceDetector = FaceDetector("FaceDetector")

    try:
        while True:
            # 100 miliseconds is an acceptable amount of input delay time.
            if FaceDetector.quit == True:
                FaceDetector.onEnd()
                break
            sleep(0.1)
    except KeyboardInterrupt:
        FaceDetector.onEnd()
        myBroker.shutdown()
        

main(robotIP, robotPort)
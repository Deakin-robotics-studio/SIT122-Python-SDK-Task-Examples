from naoqi import ALProxy, ALBroker, ALModule
from time import sleep
from random import randint

robotIP = "localhost"
robotPort = 50531

class FaceDetector(ALModule):
    
    def __init__(self, name):
        self.quit = False

        # Register our module with NAOqi
        ALModule.__init__(self, name)
        self.memory = ALProxy("ALMemory")

        # Register facial recognition module
        self.fr = ALProxy("ALFaceDetection")
        self.fr.subscribe("FaceDetector")

        # Subscribe the "onFaceDetected" function to "FaceDetected".
        self.memory.subscribeToEvent("FaceDetected",
            "FaceDetector",
            "onFaceDetected")

        self.beginRecognition()

    def onFaceDetected(self, value):
       self.stopRecognition()
       self.tts.say("I see a person!")
       sleep(1)
       self.startRecognition()

    def beginRecognition(self):
        self.fr.setRecognitionEnabled(True)

    def stopRecognition(self):
        self.fr.setRecognitionEnabled(False)

    def onEnd(self):
        self.stopRecognition()


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
                break
            sleep(0.1)
    except KeyboardInterrupt:
        FaceDetector.onEnd()
        myBroker.shutdown()
        

main(robotIP, robotPort)
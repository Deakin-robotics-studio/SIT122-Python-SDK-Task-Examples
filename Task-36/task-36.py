from naoqi import ALProxy, ALBroker, ALModule
from time import sleep

robotIP = "10.150.176.81"
robotPort = 9559
memory = None
CONFIDENCE_THRESHOLD = 0.5

class SpeechRecognition(ALModule):
    
    def __init__(self, name):
        self.quit = False
        global memory

        # Register our module with NAOqi
        ALModule.__init__(self, name)
        memory = ALProxy("ALMemory")
        self.posture = ALProxy("ALRobotPosture")
        self.tts = ALProxy("ALTextToSpeech")

        # Disable autonomous movement.
        self.am = ALProxy("ALAutonomousMoves")
        self.am.setExpressiveListeningEnabled(False)

        # Register speech recognition
        self.asr = ALProxy("ALSpeechRecognition")
        self.asr.setLanguage("English")
        self.asr.setVisualExpression(True)
        self.stopListening()
        self.asr.setVocabulary(["sit", "stand", "goodbye"], False)

        # Subscribe to the speech recognition events.
        self.asr.subscribe("SpeechRecognition")

        # Start speech recognition engine.
        self.startListening()

        # Subscribe the "onWordRecognized" function to "WordRecognized".
        memory.subscribeToEvent("WordRecognized",
            "SpeechRecognition",
            "onWordRecognized")
        
    def startListening(self):
        self.asr.pause(False)

    def onWordRecognized(self, ref, spot):
        command = spot[0]
        confidence = spot[1]

        self.stopListening()

        if confidence < CONFIDENCE_THRESHOLD:
            self.tts.say("I did not understand.")
            self.startListening()
            return

        if command == "sit":
            self.doSit()
        elif command == "stand":
            self.doStand()
        elif command == "goodbye":
            self.doQuit()
            return
        else:
            self.tts.say("I did not understand.")
        
        self.startListening()

    def doSit(self):
        self.tts.say("Yes sir.")
        self.posture.goToPosture("Sit", 1)
    
    def doStand(self):
        self.tts.say("If I must.")
        self.posture.goToPosture("Stand", 1)

    def doQuit(self):
        self.onEnd()
        
    def stopListening(self):
        self.asr.pause(True)        

    def onEnd(self):
        self.doSit()
        self.stopListening()
        self.quit = True

def main(ip, port):
    global SpeechRecognition

    # Setup the data broker.
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # Bind to socket root
       0,           # Auto-select port
       ip,          # Parent broker IP
       port)        # Parent broker port

    SpeechRecognition = SpeechRecognition("SpeechRecognition")

    try:
        while True:
            # 100 miliseconds is an acceptable amount of input delay time.
            if SpeechRecognition.quit == True:
                break
            sleep(0.1)
    except KeyboardInterrupt:
        SpeechRecognition.onEnd()
        myBroker.shutdown()
        

main(robotIP, robotPort)
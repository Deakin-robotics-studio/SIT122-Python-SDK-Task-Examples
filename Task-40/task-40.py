from naoqi import ALProxy, ALBroker, ALModule
from time import sleep
from random import randint

robotIP = "localhost"
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

        # Create an array of strings containing the numbers from 0 - 100.
        vocab = ['end game']
        for i in range(0, 100):
            vocab.append(str(i))

        # Set the robot's vocabulary to the array of strings containing the numbers.
        self.asr.setVocabulary(vocab, False)

        # Subscribe to the speech recognition events.
        self.asr.subscribe("SpeechRecognition")

        # Subscribe the "onWordRecognized" function to "WordRecognized".
        memory.subscribeToEvent("WordRecognized",
            "SpeechRecognition",
            "onWordRecognized")
        
        # Setup the game.
        self.number = -1
        self.attempts = 0
        self.beginGame()


    def beginGame(self):
        self.stopListening()
        self.number = randint(0,100)
        self.attempts = 0
        self.tts.say("I have chosen a number between zero and one-hundred.")
        self.tts.say("Can you guess what it is?")
        self.startListening()

    def endGame(self):
        self.tts.say("Congratulations. You guessed my number in %s tries." % str(self.attempts))
        self.beginGame()

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

        if command == "end game":
            self.tts.say("Goodbye.")
            self.quit = True
            return

        try:
            num = int(command)
        except:
            self.tts.say("I did not understand.")
            self.startListening()
            return

        self.attempts = self.attempts + 1

        diff = abs(num - self.number)

        if diff == 0:
            self.endGame()
        elif diff > 0 and diff < 5:
            self.tts.say("You a very close.")
        elif diff > 5 and diff < 15:
            self.tts.say("You are getting warm.")
        elif diff > 15 and diff < 35:
            self.tts.say("You are kind of close.")
        else:
            self.tts.say("You are way off!")

        self.startListening()



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

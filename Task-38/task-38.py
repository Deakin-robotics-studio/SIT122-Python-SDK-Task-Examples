from naoqi import ALProxy, ALBroker, ALModule
from time import sleep

robotIP = "localhost"
robotPort = 9559
memory = None

EVENTS = ["HandRightBackTouched", "HandLeftBackTouched", "RightBumperPressed", "LeftBumperPressed", "FrontTactilTouched"]

# The secret code in order of events
SECRET_CODE = [
    'FrontTactilTouched',
    'LeftBumperPressed',
    'RightBumperPressed',
    'LeftBumperPressed',
    'RightBumperPressed',
    'HandRightBackTouched',
    'HandLeftBackTouched',
    'FrontTactilTouched'
]

class SecretPasswordGame(ALModule):
    
    def __init__(self, name):
        global memory
        self.codeProgression = 0
        self.quit = False

        # Register our module with NAOqi
        ALModule.__init__(self, name)
        memory = ALProxy("ALMemory")
        self.tts = ALProxy("ALTextToSpeech")
       
        for k in EVENTS:
            memory.subscribeToEvent(k,
                "SecretPasswordGame",
                "onBumperPressed")

    def onBumperPressed(self, name, onOff):
        if onOff == 0: return
        self.progressCode(name)

    def progressCode(self, key):
        
        if SECRET_CODE[self.codeProgression] == key:
            self.codeProgression = self.codeProgression + 1
        else:
            self.codeProgression = 0

        self.tts.say(str(self.codeProgression))

        if self.codeProgression >= len(SECRET_CODE):
            self.onCodeComplete()
            

    def onCodeComplete(self):
        self.tts.say('Congratulations, you figured out my secret password.')
        self.codeProgression = 0
        self.tts.say('Goodbye!')
        self.quit = True

def main(ip, port):
    global SecretPasswordGame

    # Setup the data broker.
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # Bind to socket root
       0,           # Auto-select port
       ip,          # Parent broker IP
       port)        # Parent broker port

    SecretPasswordGame = SecretPasswordGame("SecretPasswordGame")

    try:
        while not SecretPasswordGame.quit:
            # 100 miliseconds is an acceptable amount of input delay time.
            sleep(0.1)
    except KeyboardInterrupt:
        myBroker.shutdown()

main(robotIP, robotPort)
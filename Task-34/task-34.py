from naoqi import ALProxy, ALBroker, ALModule
from time import sleep

robotIP = "localhost"
robotPort = 9559
memory = None

EYE_COLOR_A = 0x00FF00
EYE_COLOR_B = 0x0000FF

class FiniteStateMachine(ALModule):
    
    def __init__(self, name):
        global memory
        self.blockInput = False

        # Register our module with NAOqi
        ALModule.__init__(self, name)
        memory = ALProxy("ALMemory")
       
        memory.subscribeToEvent("RightBumperPressed",
            "FiniteStateMachine",
            "onRightBumperPressed")

        memory.subscribeToEvent("LeftBumperPressed",
            "FiniteStateMachine",
            "onLeftBumperPressed")

        self.leds = ALProxy("ALLeds")

        # States of the FSM
        self.earLedsOn = False
        self.eyeColor = EYE_COLOR_A

        # Turn stuff off.
        self.leds.fadeRGB("EarLeds", 0x000000, 0)
        self.leds.fadeRGB("FaceLeds", 0x000000, 0)

    def onLeftBumperPressed(self):
        if self.blockInput:
            return

        self.blockInput = True

        if self.earLedsOn:
            print "Turning ear LEDs off"
            self.leds.fadeRGB("EarLeds", 0x000000, 0)
            self.earLedsOn = False
        else:
            print "Turning ear LEDs on"
            self.leds.fadeRGB("EarLeds", 0x0000FF, 0)
            self.earLedsOn = True

        sleep(0.5)
        self.blockInput = False

    def onRightBumperPressed(self):
        if self.blockInput:
            return

        self.blockInput = True

        if self.eyeColor == EYE_COLOR_A:
            print "Setting eye color to B"
            self.eyeColor = EYE_COLOR_B
        else:
            print "Setting eye color to A"
            self.eyeColor = EYE_COLOR_A
        
        self.leds.fadeRGB("FaceLeds", self.eyeColor, 0)
        
        sleep(0.5)
        self.blockInput = False


def main(ip, port):
    global FiniteStateMachine

    # Setup the data broker.
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # Bind to socket root
       0,           # Auto-select port
       ip,          # Parent broker IP
       port)        # Parent broker port

    FiniteStateMachine = FiniteStateMachine("FiniteStateMachine")

    try:
        while True:
            # 100 miliseconds is an acceptable amount of input delay time.
            sleep(0.1)
    except KeyboardInterrupt:
        myBroker.shutdown()

main(robotIP, robotPort)
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

        # Register our module with NAOqi
        ALModule.__init__(self, name)
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("TouchChanged",
            "FiniteStateMachine",
            "onTouched")
        self.leds = ALProxy("ALLeds")

        # States of the FSM
        self.earLedsOn = False
        self.eyeColor = EYE_COLOR_A

    def onTouched(self, strVarName, value):

        # Unsubscribe while processing.
        memory.unsubscribeToEvent("TouchChanged",
            "FiniteStateMachine")

        for p in value:
            if not p[1] == True:
                continue
            if p[0] == "LFoot/Bumper/Left":
                self.leftBumperPressed()
            elif p[0] == "RFoot/Bumper/Right":
                self.rightBumperPressed()

        # Subscribe again to the event
        memory.subscribeToEvent("TouchChanged",
            "FiniteStateMachine",
            "onTouched")

    def leftBumperPressed(self):

        if self.earLedsOn:
            print "Turning ear LEDs off"
            self.leds.fadeRGB("EarLeds", 0x000000, 0)
            self.earLedsOn = False
        else:
            print "Turning ear LEDs on"
            self.leds.fadeRGB("EarLeds", 0x0000FF, 1)
            self.earLedsOn = True


    def rightBumperPressed(self):

        if self.eyeColor == EYE_COLOR_A:
            print "Setting eye color to B"
            self.eyeColor = EYE_COLOR_B
        else:
            print "Setting eye color to A"
            self.eyeColor = EYE_COLOR_A
        
        self.leds.fadeRGB("FaceLeds", self.eyeColor, 1)


def main(ip, port):
    global FiniteStateMachine

    # Setup the data broker.
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       ip,          # parent broker IP
       port)        # parent broker port

    FiniteStateMachine = FiniteStateMachine("FiniteStateMachine")

    try:
        while True:
            sleep(0.5)
    except KeyboardInterrupt:
        myBroker.shutdown()

main(robotIP, robotPort)
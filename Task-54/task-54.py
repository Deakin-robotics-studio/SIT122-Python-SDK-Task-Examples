from naoqi import ALProxy, ALBroker, ALModule
from time import sleep
from random import randint

robotIP = "localhost"
robotPort = 9559
memory = None
CONFIDENCE_THRESHOLD = 0.5

class InteractiveCalculator(ALModule):

    def __init__(self, name):
        global memory
        self.quit = False

        # Initiate the program mode.
        self.mode = "menu"
        self.func = ""
        self.nums = [0, 0]
        self.numCount = 0

        # Prepopulate an array that can provided as vocabulary when reading asking for numbers.
        self.numberVocab = []
        for i in range(0,100):
            self.numberVocab.append(str(i))

        # Register our module with NAOqi
        ALModule.__init__(self, name)
        memory = ALProxy("ALMemory")
        self.posture = ALProxy("ALRobotPosture")
        self.tts = ALProxy("ALTextToSpeech")

        # Disable autonomous movement.
        self.am = ALProxy("ALAutonomousMoves")
        self.am.setExpressiveListeningEnabled(False)

        # Register speech recognition
        self.asr = ALProxy("ALInteractiveCalculator")
        self.asr.setLanguage("English")
        self.asr.setVisualExpression(True)

        # Subscribe to the speech recognition events.
        self.asr.subscribe("InteractiveCalculator")

        # Subscribe the "onWordRecognized" function to "WordRecognized".
        memory.subscribeToEvent("WordRecognized",
            "InteractiveCalculator",
            "onWordRecognized")

        self.mainLoop()

    def resetCalculator(self):
        # Reset the calculator values to the default.
        self.mode = "menu"
        self.func = ""
        self.nums = [0, 0]
        self.numCount = 0

    def onEnd(self):
        self.stopListening()
        self.quit = True
        self.tts.say("Goodbye.")

    def startListening(self):
        self.asr.pause(False)

    def stopListening(self):
        self.asr.pause(True)

    def onWordRecognized(self, ref, spot):
        command = spot[0]
        confidence = spot[1]

        self.stopListening()

        if confidence < CONFIDENCE_THRESHOLD:
            self.tts.say("I did not understand.")
        else:
            # Determine what to do based on the current program mode.
            if self.mode == "menu":
                self.handleMenuResponse(command)
            elif self.mode == "input":
                self.handleInput(command)

        # Re-call the main loop.
        self.mainLoop()

    def mainLoop(self):

        # Stop the voice recognition.
        self.stopListening()

        # If a quit has been requested, do not continue.
        if self.quit == True:
            return

        # If the program is in menu mode, ask the user what to do.
        elif self.mode == "menu":
            self.giveInstructions()
            self.asr.setVocabulary(["add", "subtract", "multiply", "divide", "quit"], False)

        # If the program is in input mode, ask the user for the appropriate number.
        elif self.mode == "input":
            self.askForNumber(self.numCount + 1)
            self.asr.setVocabulary(self.numberVocab, False)

        # If the program is in calculate mode, perform a calculation.
        elif self.mode == "calculate":

            if self.func == "add":
                self.handleAddition()
            elif self.func == "subtract":
                self.handleSubtraction()
            elif self.func == "multiply":
                self.handleMultiplication()
            elif self.func == "divide":
                self.handleDivision()

            sleep(1.0)
            self.resetCalculator()
            self.mainLoop()
            return

        # Re-start the voice recognition module.
        self.startListening()

    def giveInstructions(self):
        self.tts.say("Do you want to add, subtract, multiply, divide, or quit?")

    def handleMenuResponse(self, command):
        if command == "quit":
            self.quit = True
            return

        self.func = command
        self.mode = "input"

    def askForNumber(self, num):
        if num == 1:
            self.tts.say("Okay, give me the first number between 0 and 100")
        else:
            self.tts.say("Okay, give me the second number between 0 and 100")

    def handleInput(self, command):
        num = int(command)

        # Set the number n equal to the input received.
        self.nums[self.numCount] = num
        self.numCount += 1

        # If we have collected two numbers from the user, it's time to calculate.
        if self.numCount >= 2:
            self.mode = "calculate"

    def handleAddition(self):
        self.tts.say("%s plus %s equals %s" % (str(self.nums[0]), str(self.nums[1]), str(self.nums[0] + self.nums[1]) ) )

    def handleSubtraction(self):
        self.tts.say("%s minus %s equals %s" % (str(self.nums[0]), str(self.nums[1]), str(self.nums[0] - self.nums[1]) ) )

    def handleMultiplication(self):
        self.tts.say("%s multiplied by %s equals %s" % (str(self.nums[0]), str(self.nums[1]), str(self.nums[0] * self.nums[1]) ) )

    def handleDivision(self):
        # Edge-case data validation. We cannot divide by zero!
        if self.nums[1] == 0:
            self.tts.say("Sorry. My creator wasn't brave enough to program limits into my division function.")
            self.tts.say("Therefore, I cannot devide by zero. Please try dividing by a non-zero number.")
            return

        # Allow decimals for division by re-casting a floating point number.
        num1 = self.nums[0]
        num2 = self.nums[1]
        self.nums[0] = float(num1)
        self.nums[1] = float(num2)

        self.tts.say("%s divide by %s equals %s" % (str(num1), str(num2), str(self.nums[0] / self.nums[1]) ) )

def main(ip, port):
    global InteractiveCalculator

    # Setup the data broker.
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # Bind to socket root
       0,           # Auto-select port
       ip,          # Parent broker IP
       port)        # Parent broker port

    InteractiveCalculator = InteractiveCalculator("InteractiveCalculator")

    try:
        while True:
            # 100 miliseconds is an acceptable amount of input delay time.
            if InteractiveCalculator.quit == True:
                InteractiveCalculator.onEnd()
                break
            sleep(0.1)
    except KeyboardInterrupt:
        InteractiveCalculator.onEnd()
        myBroker.shutdown()


main(robotIP, robotPort)

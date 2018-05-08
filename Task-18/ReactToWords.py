from naoqi import ALProxy, ALBroker, ALModule
from time import sleep

robotIP = "localhost"
robotPort = 9559
CONFIDENCE_THRESHOLD = 0.3

class SpeechRecognition(ALModule):

	def __init__(self, name):
		# Register our module with naoqi
		ALModule.__init__(self, name)

		self.memory = ALProxy("ALMemory")

		self.asr = ALProxy("ALSpeechRecognition")
		self.asr.setLanguage("English")
		self.asr.setVocabulary(["yes", "no"], False)
		self.asr.subscribe("SpeechRecognition")
		self.asr.pause(False)

		self.tts = ALProxy("ALTextToSpeech")

		# Subscribe self.onWordRecognized to WordRecognized.
		self.memory.subscribeToEvent("WordRecognized", "SpeechRecognition", "onWordRecognized")

	def onWordRecognized(self, ref, spot):
		command = spot[0]
		confidence = spot[1]
		print "I heard %s with a confidence level of %s" % (command, confidence)
		self.tts.say(command)

	def onEnd(self):
		self.asr.pause(True)
		self.quit = True

def main(ip, port):
        global SpeechRecognition

        # Setup the data broker.
        myBroker = ALBroker("myBroker", "0.0.0.0", 0, ip, port)
        SpeechRecognition = SpeechRecognition("SpeechRecognition")
        try:
                while True:
                        sleep(0.1)
        except KeyboardInterrupt:
                SpeechRecognition.onEnd()
                myBroker.shutdown()

if __name__ == "__main__":
	main(robotIP, robotPort)

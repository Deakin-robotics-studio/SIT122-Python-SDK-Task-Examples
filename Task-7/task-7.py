from time import sleep
from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "192.168.48.210", 9559)

tts.setParameter("speed", 50)
tts.setParameter("pitchShift", -1.5)
tts.say("Sometimes it's lonely being a robot.")

# Wait five seconds before continuing.
sleep(5)

tts.resetSpeed()
tts.setParameter("pitchShift", 1.5)
tts.say("But then I remember I don't have real feelings and feel better.")

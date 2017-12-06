from time import sleep
from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "localhost", 9559)

tts.setParameter("speed", 50)
tts.setParameter("pitchShift", 1)
tts.say("Sometimes it's lonely being a robot.")

# Wait three seconds before continuing.
sleep(3)

tts.resetSpeed()
tts.setParameter("pitchShift", 1.2)
tts.say("But then I remember I don't have real feelings and feel better.")

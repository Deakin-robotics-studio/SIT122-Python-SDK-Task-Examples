from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "localhost", 9559)
tts.say("Hello world")

from time import sleep
from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "localhost", 9559)

# Robot voice, speed 200.
tts.setParameter("speed", 200)
tts.say("Now, look, let's start with the three fundamental Rules of Robotics - the three rules that are built most deeply into a robot's positronic brain.")
sleep(1.5)
tts.say("We have: One, a robot may not injure a human being, or, through inaction, allow a human being to come to harm.")
sleep(0.5)

# Human voice, reset the speed and increase the pitch.
tts.resetSpeed()
tts.setParameter("pitchShift", 1.5)
tts.say("Right!")
sleep(1.0)

# Robot voice, reset the pitch.
tts.setParameter("pitchShift", 0)
tts.say("a robot must obey the orders given it by human beings except where such orders would conflict with the First Law.")
sleep(0.5)

# Human voice, increase the pitch.
tts.setParameter("pitchShift", 1.5)
tts.say("Right!")
sleep(1.0)

# Robot voice, reset the pitch.
tts.setParameter("pitchShift", 0)
tts.say("And three, a robot must protect its own existence as long as such protection does not conflict with the First or Second Laws.")
sleep(0.5)

# Human voice, increase the pitch.
tts.setParameter("pitchShift", 1.5)
tts.say("Right!")
sleep(3)
tts.say("Now where are we?")
sleep(1)

# Robot voice, reset the pitch.
tts.setParameter("pitchShift", 0)
tts.say("Exactly at the explanation. The conflict between the various rules is ironed out by the different positronic potentials in the brain. We'll say that a robot is walking into danger and knows it. The automatic potential that Rule 3 sets up turns him back. But suppose you order him to walk into that danger. In that case, Rule 2 sets up a counterpotential higher than the previous one and the robot follows orders at the risk of existence.")

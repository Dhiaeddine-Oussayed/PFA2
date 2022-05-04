from pyttsx3 import init
from time import time, sleep


def change_voice(eng, language, gender='VoiceGenderFemale'):
    for voice in eng.getProperty('voices'):
        if language in voice.languages and gender == voice.gender:
            eng.setProperty('voice', voice.id)
            return True


engine = init()
change_voice(engine, 'en_US', "VoiceGenderFemale")


def talk(speech):
    print('Assistance: ', speech)
    engine.say(speech)
    engine.runAndWait()

start = time()
timer_time = 10
sleep(timer_time-8.349)
talk('Your timer finishes in 5 seconds')
for i in range(5):
    sleep(1)
    print("Timer finished in ", 5 - i)
end = time()

print(end-start)


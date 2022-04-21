import json
import os

DATA_DIRECTORY = 'data'
ALL_DATA = []
for file in os.listdir(DATA_DIRECTORY):
    f = open(os.path.join(DATA_DIRECTORY, file))
    ALL_DATA.append(json.load(f))
    f.close()

targets = ['volumeDown', 'volumeUp']
data_from_0 = []
for i in targets:
    for j in ALL_DATA[0]['sentences']:
        if j['intent'] == i:
            data_from_0.append([j['text'], i])

intent = ['Greeting', 'CourtesyGreeting', 'NameQuery', 'UnderstandQuery',
          'Shutup', 'CourtesyGoodBye', 'WhoAmI', 'SelfAware', 'GoodBye']
data_from_1 = []
for i in ALL_DATA[1]['intents']:
    if i['intent'] in intent:
        for j in i['text']:
            data_from_1.append([j, i['intent']])

intentions = ['meeting_schedule', 'next_song', 'play_music', 'reminder', 'repeat',
              'spelling', 'tell_joke', 'thank_you', 'time', 'timer', 'alarm', 'calculator', 'calendar',
              'date', 'definition', 'translate', 'user_name', 'weather', 'what_can_i_ask_you']
data_from_2 = []
for i in intentions:
    for j in ALL_DATA[2]:
        if j[1] == i:
            data_from_0.append([j[0], i])

dataset = data_from_0 + data_from_1 + data_from_2

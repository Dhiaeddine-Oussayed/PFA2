import audioread
from pygame import mixer
import os
from time import sleep
from threading import Thread, Event

_exit = Event()
mixer.init()

path = '/Users/dhiaoussayed/Music/Music/Media.localized/Music/Unknown Artist/Unknown Album'
playlist = [os.path.join(path, music) for music in os.listdir(path)]

index = 0
stop_threads = False
def play_music():
    global index
    while 1:
        mixer.music.load(playlist[index])
        mixer.music.play()
        with audioread.audio_open(playlist[index]) as f:
            length = f.duration
        _exit.wait(length)
        index += 1
        if index >= len(playlist):
            index = 0

        if stop_threads:
            break
music_thread = Thread(target=play_music)
music_thread.start()

while True:
    print("------------------------------------------------------------------------------------")
    print("Press 'p' to pause the music")
    print("Press 'r' to resume the music")
    print("Press 'e' to exit the program")

    # take user input
    userInput = input(" ")

    if userInput == 'p':

        # Pause the music
        mixer.music.pause()
        print("music is paused....")
    elif userInput == 'r':

        # Resume the music
        mixer.music.unpause()
        print("music is resumed....")
    elif userInput == 'e':

        # Stop the music playback
        mixer.music.stop()
        print("music is stopped....")
        stop_threads = True
        _exit.set()
        break


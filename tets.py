from pygame import mixer
import os



# Instantiate mixer
mixer.init()

# Play the music
for i in range(len(playlist)):
    mixer.music.load(os.path.join(path, playlist[i]))
    mixer.music.play()


# Infinite loop
while True:
    print("------------------------------------------------------------------------------------")
    print("Press 'p' to pause the music")
    print("Press 'r' to resume the music")
    print("Press 'e' to exit the program")

    # take user input
    userInput = input(" ")

    if userInput == 'p':
        i+=1
        if i>2:
            i=0
        # Pause the music
        mixer.music.load(os.path.join(path, playlist[i]))
        mixer.music.play()
        print(i)
    elif userInput == 'r':

        # Resume the music
        mixer.music.unpause()
        print("music is resumed....")
    elif userInput == 'e':

        # Stop the music playback
        mixer.music.stop()
        print("music is stopped....")
        break

import os, vlc, time, csv, sys
from mutagen.mp3 import MP3
import RPi.GPIO as GPIO
from os import system, name

path_to_files = 'kuma_shadow/files' #where sound files are stored
path_to_toc = 'kuma_shadow/file_toc.txt' #table of contents produced from toc_maker.py
path_to_history = 'kuma_shadow/history.txt' #for now, just store last played track number

def clear():
    os.system('cls||clear')

def exit():
    sys.exit("Exiting")
    
def play_track(file): # to play the file
    toc = [] #blank 
    with open(path_to_toc, 'r') as f:
        linereader = csv.reader(f, delimiter=';')
        for line in linereader:
            toc.append(line) #create a list of all items in TOC, track number and name
        f.close

    with open(path_to_history, 'r') as f:
        last_item = f.read()
        f.close

    file_to_play = toc[int(last_item)-1][1]
    print(file_to_play + ' play_track #1')

    # file_to_play = str(file)
    path = os.path.join(path_to_files, file_to_play) #combines path to folder and file name generated to find file name to play
    print(path + ' after play_track #2') #for troubleshooting
    media = vlc.MediaPlayer(path) #sets VLC to play the file at it's path
    audio = MP3(path) #using MP3 from mutagen to find length of audio file
    play_time = audio.info.length #sets variable to time length of file
    media.play() #play the file in VLC
    print(str(play_time)) #print length of file in seconds
    time.sleep(play_time) #sets sleep value to the length of the track.  Used with .stop() below
    media.stop() #declared to definitively stop playback.  If not set it will shutdown vlc the instant it is started providing no output

def update_history(): #checks if history is available; if so updates history based on latest; if not, starts from zero on file_toc.txt
    toc = [] #blank 
    with open(path_to_toc, 'r') as f:
        linereader = csv.reader(f, delimiter=';')
        for line in linereader:
            toc.append(line) #create a list of all items in TOC, track number and name
        f.close

    first_item = toc[0][0] #find the first item's item number

    if os.path.exists(path_to_history): #check if history.txt exists, if it does, pull latest item
            with open(path_to_history, 'r') as f:
                last_item = str(f.read())
                f.close
    else:
        with open(path_to_history, 'w') as f: #if history.txt does not exist, create it and put in item #1 from TOC
            f.write(first_item)
            f.close

    global file #set global variable of item number
    file = toc[int(last_item)][1]
    print(file + ' after history is called #1')

def next_track(item):
    with open(path_to_history, 'r') as f: 
        item = int(f.read())
        f.close
        item +=1
        with open(path_to_history, 'w') as f:
            f.write(str(item))
            f.close
    play_track(file)

def prev_track(item):
    with open(path_to_history, 'r') as f: 
        item = int(f.read())
        f.close
        item = item - 1
        with open(path_to_history, 'w') as f:
            f.write(str(item))
            f.close
    play_track(file)


#Setup up GPIO for use
update_history()
print(file + ' after history is updated #2')
GPIO.setwarnings(False) #Ignore warnings
GPIO.setmode(GPIO.BCM) #set the gpios to read as on the pi
channel_list =[13, 22, 27, 5, 24] #channels being used
GPIO.cleanup(channel_list)
GPIO.setup(channel_list, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# The above sets all the channels as inputs and pulls them down on startup.  Otherwise they always read high.

GPIO.add_event_detect(13,GPIO.RISING,callback=play_track) # Setup event on pin 10 rising edge
GPIO.add_event_detect(22,GPIO.RISING,callback=next_track) # Setup event on pin 10 rising edge
GPIO.add_event_detect(27,GPIO.RISING,callback=prev_track) # Setup event on pin 10 rising edge

message = input("Press enter to quit\n\n") # Run until someone presses enter

GPIO.cleanup() # Clean up

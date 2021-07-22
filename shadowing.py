import os, vlc, time, csv, sys
from mutagen.mp3 import MP3
import RPi.GPIO as GPIO
from os import system, name
from waveshare_epd import epd2in13_V2
from PIL import Image,ImageDraw,ImageFont

def clear():
    os.system('cls||clear')

def exit():
    sys.exit("Exiting")

def create_toc(file_toc):
    global toc #set a global to be used in other functions
    toc = [] #empty list for toc
    with open(file_toc, 'r') as f:
        linereader = csv.reader(f, delimiter=';')
        for line in linereader:
            toc.append(line) #create a list of all items in TOC, track number and name
        f.close

def update_history(file_history): #checks if history is available; if so updates history based on latest; if not, starts from zero on file_toc.txt

    first_item = toc[0][0] #find the first item's item number

    if os.path.exists(file_history): #check if history.txt exists, if it does, pull latest item
            with open(file_history, 'r') as f:
                current_item = str(f.read())
                f.close
    else:
        with open(file_history, 'w') as f: #if history.txt does not exist, create it and put in item #1 from TOC
            f.write(first_item)
            f.close

    global play_file #set global variable of item number
    play_file = toc[int(current_item)][1]
    return play_file
    print(play_file + ' is current track')

def play_track(click, play_file): # to play the file
    # #First play click
    media = vlc.MediaPlayer(click) #sets VLC to play the file at it's path
    #audio = MP3(click) #using MP3 from mutagen to find length of audio file
    play_time = 0.5 #sets variable to time length of file
    media.play() #play the file in VLC
    time.sleep(play_time) #sets sleep value to the length of the track.  Used with .stop() below
    media.stop() #declared to definitively stop playback.  If not set it will shutdown vlc the instant it is started providing no output
    time.sleep(0.5)

    #Now play shadowing track
    media = vlc.MediaPlayer(play_file) #sets VLC to play the file at it's path
    audio = MP3(play_file) #using MP3 from mutagen to find length of audio file
    play_time = audio.info.length #sets variable to time length of file
    media.play() #play the file in VLC
    print(str(play_time)) #print length of file in seconds
    time.sleep(play_time) #sets sleep value to the length of the track.  Used with .stop() below
    media.stop() #declared to definitively stop playback.  If not set it will shutdown vlc the instant it is started providing no output
    time.sleep(0.5)

def next_track(file_history):
    with open(file_history, 'r') as f: 
        item = int(f.read())

        item +=1

    with open(file_history,'w') as f:
        f.write(str(item))

def prev_track(file_history):
    with open(file_history, 'r') as f: 
        item = int(f.read())

        item +=-1
        
    with open(file_history,'w') as f:
        f.write(str(item))


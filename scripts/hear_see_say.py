from logging import shutdown
import sys, os, time, csv, vlc, yaml
from mutagen.mp3 import MP3

#########################
# Directories and files #
#########################

dir_audio = '../audio/' # directory with all audio.  no sub dirs.
dir_fonts = '../pics/' # directory with fonts. no sub dirs.
file_history = '../files/history.txt' # keep track of current track
file_toc = '../files/file_toc.txt' # TOC of audio files
file_script = '../files/script.yaml'
click = '../files/click.wav'

#############
# Pin Setup #
#############

pin_play = 13 # Use BCM channel
pin_next = 22 # Use BCM channel
pin_prev = 27 # Use BCM channel
pin_shutdown = 5 # Use BCM channel
pin_volup = 24 # Use BCM channel
pin_voldn = 3 # Use BCM channel
channel_list =[pin_play, pin_next, pin_prev, pin_shutdown, pin_voldn, pin_volup] # Complete list

#################
# Function list #
#################

def clear(): # Setup function to clear terminal screens
    os.system('cls||clear')

def exit(): # Setup function to elegantly exit
    sys.exit("Exiting")

def create_toc(file_toc): # Create the TOC off of the file structure
    global toc
    toc = [] #empty list for toc
    with open(file_toc, 'r') as f:
        linereader = csv.reader(f, delimiter=';')
        for line in linereader:
            toc.append(line) #create a list of all items in TOC, track number and name
        f.close
    return toc

def find_filename(file_history): # Find file name in the TOC to go with track number, used for media play
    global play_file
    with open(file_history, 'r') as f:
        play_file = str(f.read())
        f.close
    play_file = toc[int(track_num)][1]
    return play_file

def read_script():
    clear()

    name = play_file.replace('.mp3', '')

    with open(file_script, 'r') as file:
        script = yaml.safe_load(file)
        for each in script[name]['japanese']:
            print(script[name]['japanese'][each])
        print('\n')
        for each in script[name]['english']:
            print(script[name]['english'][each])
#        print(script[name]['japanese'])
#        print(script[name]['english'])
    file.close

def update_history(file_history): #checks if history is available; if so updates history based on latest; if not, starts from zero on file_toc.txt
    global track_num
    if os.path.exists(file_history): #check if history.txt exists, if it does, pull latest item
        with open(file_history, 'r') as f:
            track_num = f.read()
    else:
        with open(file_history, 'w') as f: #if history.txt does not exist, create it and put in item #1 from TOC
            track_num = toc[0][0] #set the first item in the toc as track number
            f.write(track_num)
            f.close
    return track_num

def find_file():
    global play_file
    play_file = toc[int(track_num)][1]
    return play_file

def play_track(): # Play file for shadowing
    play_file = find_file()
    #read_script()
#    play_file = toc[int(track_num)][1]p
#    play_file = find_filename(file_history)
#    print(play_file)
    # Play the click before each track
    media = vlc.MediaPlayer(click) #sets VLC to play the file at it's path
    play_rate = .9
    adjust_time = 1-play_rate #sets variable to time length of file
    time.sleep(1) # sometimes click doesn't play, maybe buffering?
    media.play() #play the file in VLC
    time.sleep(1) #sets sleep value to the length of the track.  Used with .stop() below
    media.stop() #declared to definitively stop playback.  If not set it will shutdown vlc the instant it is started providing no output
    time.sleep(0.5) # slight pause after playback to keep next track from interfering

    # Now play shadowing track
    media = vlc.MediaPlayer("../audio/"+play_file) #sets VLC to play the file at it's path
    audio = MP3("../audio/"+play_file) #using MP3 from mutagen to find length of audio file
    play_time = audio.info.length #sets variable to time length of file
    media.set_rate(play_rate)
    media.play() #play the file in VLCp
    time.sleep(play_time*(1+adjust_time)) #sets sleep value to the length of the track.  Used with .stop() below
    media.stop() #declared to definitively stop playback.  If not set it will shutdown vlc the instant it is started providing no output
    time.sleep(0.5) # slight pause after playback to keep next track from interfering

def next_track():
    global track_num
    track_num = int(update_history(file_history))
    with open(file_history, 'w') as f: 
        track_num +=1
        f.write(str(track_num))
    f.close()
    print(find_file())
    return track_num
    play_track()

def prev_track():
    global track_num
    track_num = int(update_history(file_history))
    with open(file_history, 'w') as f: 
        track_num +=-1
        f.write(str(track_num))
    f.close()
    print(find_file())
    return track_num
    play_track()

# def splash_screen(logo, top, bottom):
#     # Display the splash screen
#     epd.init(epd.FULL_UPDATE) #Performs full update to prevent ghosting/burn-in
#     epd.Clear(0xFF) #Clears the screen
#     logo_text = '???'
#     side_text_top = 'KUMA'
#     side_text_bot = 'SHADOW'
#     pass

def write_screen():
    pass

def find_trackpath(file_history, dir_audio):
    track = find_filename(file_history, track_num)
    track_path = str(dir_audio+track)
    return track_path

def shut_down(): # Shutdown the machine elegantly
    update_history()
    shutdown_script.shutdown(pin_shutdown)

####################
# Start up process #
####################

# Create TOC every startup to capture any changes to files
try:
    create_toc(file_toc)
    update_history(file_history) # also update history file
    print('Table of Contents created')
    find_file()
except ValueError:
    print('Error in creating TOC')

#Set some GPIO flags, create a list of input pins to use, then set them up as input pins
# GPIO.setwarnings(False) #Ignore warnings
# GPIO.setmode(GPIO.BCM) #set the gpios to read as on the pi
# GPIO.cleanup(channel_list) #sets them all to 0 for a clean start
# GPIO.setup(channel_list, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #sets all the channels as inputs and pulls them down on startup.  Otherwise they always read high.

# GPIO.setup(channel_list, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #sets all the channels as inputs and pulls them down on startup.  Otherwise they always read high.
# GPIO.add_event_detect(pin_play,GPIO.FALLING,callback=play_track) # Setup event on pin 10 FALLING edge
# GPIO.add_event_detect(pin_next,GPIO.FALLING,callback=next_track) # Setup event on pin 10 FALLING edge
# GPIO.add_event_detect(pin_prev,GPIO.FALLING,callback=prev_track) # Setup event on pin 10 FALLING edge
# GPIO.add_event_detect(pin_shutdown,GPIO.FALLING,callback=shut_down) # Setup event on pin 10 FALLING edge


while True:
    #Set up what each pin will do
    
    time.sleep(0.01)
    #GPIO.add_event_detect(pin_volup,GPIO.FALLING,callback=vol_up) # Setup event on pin 10 FALLING edge
    #GPIO.add_event_detect(pin_voldn,GPIO.FALLING,callback=vol_down) # Setup event on pin 10 FALLING edge

    #Also setup for keyboard inputs
    # Uncomment if needed
    if __name__ == "__main__":
        start_message = input('Do you want to rebuild the Table of Contents?')
        if start_message.lower == 'y':
            create_toc()

        update_history(file_history)
        find_file()
        message = input('(P)lay (R)ead (N)ext (L)ast (Q)uit\n')
        while True:
            message = input()
            if message == 'p':
                find_file()
                print(play_file)
#                clear()
#                read_script()
                play_track()
                print('\n')
                clear()
                print('(P)lay (R)ead (N)ext (L)ast (Q)uit\n')
            elif message == 'r':
                print(play_file)
                read_script()
                play_track()
                print('\n')
                clear()
                print('(P)lay (R)ead (N)ext (L)ast (Q)uit\n')
            elif message == 'n' :
                next_track()
                find_file()
                play_track()
                clear()
                print('(P)lay (R)ead (N)ext (L)ast (Q)uit\n')
            elif message == 'l' :
                prev_track()
                find_file()
                play_track()
                clear()
                print('(P)lay (R)ead (N)ext (L)ast (Q)uit\n')
            elif message == 'q' :
                # GPIO.cleanup() # Clean up
                exit()


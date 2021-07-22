import shadowing
import RPi.GPIO as GPIO

dir_audio = 'audio/' # directory with all audio.  no sub dirs.
dir_fonts = 'pics/' # directory with fonts. no sub dirs.
file_history = 'files/history.txt' # keep track of current track
file_toc = 'files/file_toc.txt' # TOC of audio files
file_script = 'files/script.yaml'
click = 'files/click.wav'

history_init = 0

#Sets up history file if not already setup.
if history_init == 0:
    shadowing.create_toc(file_toc)
    shadowing.update_history(file_history)
    history_init = 1
    print('History file OK.')
    #Set some GPIO flags, create a list of input pins to use, then set them up as input pins
    GPIO.setwarnings(False) #Ignore warnings
    GPIO.setmode(GPIO.BCM) #set the gpios to read as on the pi
    channel_list =[13, 22, 27, 5, 24, 3] #channels being used
    GPIO.cleanup(channel_list) #sets them all to 0 for a clean start
    GPIO.setup(channel_list, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #sets all the channels as inputs and pulls them down on startup.  Otherwise they always read high.
    shadowing.create_toc(file_toc)
else:
    print('History failed to update.  Check code or file and try again.')
    shadowing.exit()

def play():
    track = shadowing.update_history(file_history)
    track_path = str(dir_audio+track)
    shadowing.play_track(click, track_path)

def next():
    shadowing.next_track(file_history)
    track = shadowing.update_history(file_history)
    track_path = str(dir_audio+track)
    shadowing.play_track(click, track_path)

def prev():
    shadowing.prev_track(file_history)
    track = shadowing.update_history(file_history)
    track_path = str(dir_audio+track)
    shadowing.play_track(click, track_path)

#Set up what each pin will do
GPIO.add_event_detect(13,GPIO.RISING,callback=play) # Setup event on pin 10 rising edge
GPIO.add_event_detect(3,GPIO.RISING,callback=next) # Setup event on pin 10 rising edge
GPIO.add_event_detect(5,GPIO.RISING,callback=prev) # Setup event on pin 10 rising edge

#Also setup for keyboard inputs
if __name__ == "__main__":
    while True:
        message = input('(P)lay (N)ext (L)ast (Q)\n')
        if message == 'p':
            play()
        elif message == 'n' :
            next()
        elif message == 'l' :
            prev()
        elif message == 'q' :
            shadowing.exit()

GPIO.cleanup() # Clean up

#Setup screen and start display
#update_history()
#print(file + ' after history is updated #2')

# Dimensions of screen
x = 249
y = 121

epd = epd2in13_V2.EPD() #Sets the driver to use

epd.init(epd.FULL_UPDATE) #Performs full update to prevent ghosting/burn-in
epd.Clear(0xFF) #Clears the screen

# Drawing on the image
font10 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 10)
font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
font72 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 72)
    
font72 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 72)
    
image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame  $
draw = ImageDraw.Draw(image)
    
#Draw text
    
#First make text for radio information
draw.text((1,1), 'Boot complete, ready to run.', font = font10, fill = 0)

#Now draw outlines and text to screen
epd.display(epd.getbuffer(image))

# Display track

#setup GPIO for use
GPIO.setwarnings(False) #Ignore warnings
GPIO.setmode(GPIO.BCM) #set the gpios to read as on the pi
channel_list =[13, 22, 27, 5, 24] #channels being used
GPIO.cleanup(channel_list)
GPIO.setup(channel_list, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# The above sets all the channels as inputs and pulls them down on startup.  Otherwise they always read high.

GPIO.add_event_detect(13,GPIO.RISING,callback=shadowing.play_track) # Setup event on pin 10 rising edge
GPIO.add_event_detect(22,GPIO.RISING,callback=next_track) # Setup event on pin 10 rising edge
GPIO.add_event_detect(27,GPIO.RISING,callback=prev_track) # Setup event on pin 10 rising edge

# Add keyboard functionality for testing


message = input("Press enter to quit\n\n") # Run until someone presses enter

GPIO.cleanup() # Clean up

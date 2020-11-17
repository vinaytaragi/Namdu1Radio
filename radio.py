#but11!/usr/bin/python
# @brief: Script to record and upload the audio files
#         GPIO's are used for recording and uploading
#         LED's  used for indicating respective category
#
# @ver: 1.0
#----------------------------------------------------------------#
# ##   # #### ##   ## ###  #  #  ##  ####   #### ###  ##### #### #
# # #  # #  # # # # # #  # #  # # #  #   #  #  # #  #   #   #  # #
# #  # # #**# #  #  # #  # #  #   #  ####   #### #  #   #   #  # #
# #   ## #  # #     # ###  ####  ### #    # #  # ###  ##### #### #
#----------------------------------------------------------------#
# *** Libraries *** #
import RPi.GPIO as GPIO
from gpiozero import LED, Button
import time
import os
import socket
import subprocess
import wave
import contextlib
from datetime import datetime
from subprocess import check_output
import shutil
from dualled import DualLED

# *** Global Variables *** #
previousTime = False
but1n2_pressed = False
ret = "Hello"
radio = False
duration = 5
genplaypause = True
# flag to check if button is pressed and held for long time
longpress = False 
longpress2 = False
# flag to monitor if radio is on or off
nammaschoolradio = True
#Variable to start the radio at the begining automatically
cntr = True
#Variable to used to start/stop the radio on button press
playpause = False
#Flag to monitor pendrive state
penDet = False
#Categories play and pause flags
cat1playpause = False
cat2playpause = False
cat3playpause = False
cat4playpause = False
cat5playpause = False
cat6playpause = False
cat7playpause = False
cat8playpause = False
cat9playpause = False
cat10playpause = False
cat1preview = False
cat2preview = False
cat3preview = False
cat4preview = False
cat5preview = False
cat6preview = False
cat7preview = False
cat8preview = False
cat9preview = False
cat10preview = False
gencatpreview = False
# network verification variables
remote_server = "www.google.com"
local_server = "192.168.1.50"
recFileName = "record"

# setting folder paths
projectpath =  os.path.split(os.path.realpath(__file__))[0]
audioguidepath = projectpath + "/audio-alert"
previewaudioguidepath = projectpath + "/recordings"
#local categories .wav file save path
recordingpath1to9 = projectpath + "/recordings/cat"
recordingpathcat1 = projectpath + "/recordings/cat1"
recordingpathcat2 = projectpath + "/recordings/cat2"
recordingpathcat3 = projectpath + "/recordings/cat3"
recordingpathcat4 = projectpath + "/recordings/cat4"
recordingpathcat5 = projectpath + "/recordings/cat5"
recordingpathcat6 = projectpath + "/recordings/cat6"
recordingpathcat7 = projectpath + "/recordings/cat7"
recordingpathcat8 = projectpath + "/recordings/cat8"
recordingpathcat9 = projectpath + "/recordings/cat9"
recordingpathcat10 = projectpath + "/recordings/cat10"
recordingpathcat11 = projectpath + "/recordings/gencat"
#.upload categories .mp3 file save path
uploadpath = "/var/www/html/.upload"
uploadpath1to9 = uploadpath + "/cat"
uploadpathcat1 = uploadpath + "/cat1"
uploadpathcat2 = uploadpath + "/cat2"
uploadpathcat3 = uploadpath + "/cat3"
uploadpathcat4 = uploadpath + "/cat4"
uploadpathcat5 = uploadpath + "/cat5"
uploadpathcat6 = uploadpath + "/cat6"
uploadpathcat7 = uploadpath + "/cat7"
uploadpathcat8 = uploadpath + "/cat8"
uploadpathcat9 = uploadpath + "/cat9"
uploadpathcat10 = uploadpath + "/cat10"
uploadpathcat11 = uploadpath + "/gencat"

''' *** Global Functions *** '''
'''
    To check if Pi is connected to internet or local server
'''
def is_connected(network):
    try:
        #if ".com" in network:
        #    network = socket.gethostbyname(network)
        s = socket.create_connection((network, 80))
        return True
    except:
        return False

''' To check if wifi is local network '''        
def is_onradio():
    try:
        test = "Namdu1Radio" in check_output("iwgetid", universal_newlines=True)
        return test
    except:
        return False

'''
    Macro for playing audio instructions - to keep the code simple
'''
def aplay(filename):
    os.system("aplay "+audioguidepath+"/"+filename)
    
'''
    Macro for playing recorded audio
'''
def previewplay(path, filename):
    os.system("aplay "+path+"/"+filename+ "&")
    
    '''
    Macro for recording audio
'''
def arecord(path, filename):
    os.system("arecord "+path+"/"+filename+" -D sysdefault:CARD=2 -f dat &")
    
'''
    For the given path, get the List of all files in the directory tree 
'''
def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles

'''
    Function to shutdown pi
'''    
def shutdownPi():
    os.system("pkill -9 aplay")
    aplay("shutdown.wav")
    os.system("sleep 3s; shutdown now ")                                
    exit(0)

'''
    Function to join wavefiles
'''    
#def wavFilesJoin(file1,file):
    #a, fs, enc = audiolab.wavread('file1')
    #b, fs, enc = audiolab.wavread('file2')
    #c = scipy.vstack((a,b))
    #audiolab.wavwrite(c, 'file3.wav', fs, enc)
    #return file3.wav

#LED's config:
#------------
led1 = LED(18) #GPIO18 - LED1
led2 = LED(23) #GPIO23 - LED2
#led3 = LED(24) #GPIO24 - LED3
led4 = LED(25) #GPIO25 - LED4
led5 = LED(8)  #GPIO8  - LED5
led6 = LED(7)  #GPIO7  - LED6
led7 = LED(12) #GPIO12 - LED7
led8 = LED(16) #GPIO16 - LED8
led9 = LED(20) #GPIO20 - LED9
#led11 = LED(21) #GPIO21 - LED11
led10 = LED(14) #GPIO14 - LED10

led = None
led = DualLED(21,24)

#GPIO's config:
#-------------
but1 = Button(17) #17 - cat1
but2 = Button(27) #27 - cat2
but3 = Button(22) #22 - cat3
but4 = Button(10) #10 - cat4
but5 = Button(9)  #9  - cat5
but6 = Button(11) #11 - cat6
but7 = Button(5)  #5  - cat7
but8 = Button(6)  #6  - cat8
but9 = Button(13) #13 - cat9
but10 = Button(19)#19 - cat10
but11 = Button(26)#26 - cat11

# *** Setting up GPIO of Pi *** #
GPIO.setmode(GPIO.BCM)
#time.sleep(10.0)
led.fwd_on()
#Pi started indication audio
print("pi Started")
#Test folder to verify local backup play
aplay("lappiready.wav")
#time.sleep(3.0)
while True:
    print("pi Running")
    #led.off()
    #led.fwd_on()
    #Check whether local server connected
    if is_onradio() and is_connected(local_server) and cntr:
        os.system("pkill -9 aplay")
        time.sleep(0.1)
        print ("starting namma school radio....from local server ")
        aplay("radiostart.wav")
        #time.sleep(3)
        os.system("chromium-browser --kiosk --app=http://"+local_server+" &")        
        cntr = False
        playpause = True
    #Check whether the internet is available to play from the website
    elif is_connected(remote_server) and cntr:
        print ("starting namma school radio from internet")
        os.system("pkill -9 aplay")
        #time.sleep(3)
        aplay("radiostart.wav")
        os.system("chromium-browser --kiosk --app=http://stream.zeno.fm/ghuhx13nf5zuv &")
        time.sleep(1.0)
        os.system('rclone mount gdrive: $HOME/mnt/gdrive &')
        time.sleep(5.0)
        cntr = False
        playpause = True
    elif cntr == True:
        print ("Local and remote server not available")
        print ("Audio starts from localhost")
        os.system("pkill -9 aplay")
        src_renamPath = r'/var/www/html/indexgencat.php'
        dst_renamPath = r'/var/www/html/index.php'
        shutil.copy(src_renamPath, dst_renamPath)
        #time.sleep(3)
        aplay("radiostart.wav")
        os.system("chromium-browser --kiosk localhost &")
        cntr = False
        playpause = True
        time.sleep(0.2)

    ''' if button1 is pressed - Category 1 functionality button '''
    if but1.is_pressed:
        print("button1 pressed")
        previousTime = time.time()
        while but1.is_pressed:
            #Check if the button is pressed for > 2sec
            if time.time() - previousTime > 2.0:
                if((but2.is_pressed) or (but3.is_pressed) or (but4.is_pressed)or  
                (but5.is_pressed) or (but6.is_pressed) or (but7.is_pressed) or 
                (but8.is_pressed) or (but9.is_pressed) or (but10.is_pressed) or (but11.is_pressed)):
                    #if any of the buttons 2 to 9 is also pressed and held, then shutdown the Pi
                    shutdownPi()
                #if the button is pressed for more than two seconds, then longpress is True
                longpress = True
                aplay("beep_cat1.wav")
                #break
        if time.time() - previousTime < 0.1: continue
        time.sleep(0.5)
        if longpress:
            led1.on()
            os.system("killall chromium-browser")
            os.system("pkill -o chromium")
            #time.sleep(0.4)
            #os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
            #aplay("beep_cat1.wav")
            time.sleep(1.0)
            # records with 48000 quality
            arecord("recorded_audio.wav") 
            # scan for button press to stop recording
            but1.wait_for_press()
            os.system("pkill -9 arecord")
            os.system("pkill -9 aplay")
            time.sleep(0.4)
            aplay("Cat1_stop.wav")
            print("Cat1 recording stopped")
            time.sleep(5.0)
            previewplay("recorded_audio.wav")
            recFileName = "recorded@"+datetime.now().strftime('%d%b%Y_%H_%M_%S')
            # converting recorded audio to mp3 and rename with date and time of recording
            os.system("lame -b 320 "+previewaudioguidepath+"/recorded_audio.wav " +recordingpathcat1+"/"+recFileName+".mp3")
            #save the recorded audio in .upload folder respective category
            os.system("sudo cp "+recordingpathcat1+"/"+recFileName+".mp3 " +uploadpathcat1+"/"+recFileName+".mp3 &")
            os.system("pkill -9 aplay")            
            #os.system("rm "+recordingpathcat1+"/recorded_audio.wav") #remove the recorded file
            longpress = False
            cat1playpause = True
            cat1preview = True
            led1.off()
            #break
        else:
            led1.on()
            pfiles = os.listdir(uploadpathcat1)
            if cat1preview == True:
                cat1preview = False
                print("Cat1 preview stopped")
                os.system("pkill -9 aplay")
            elif cat1playpause == True:
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("radiostop.wav")
                cat1playpause = False
                playpause = False
            elif is_connected(remote_server):
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                print ("starting namma school radio from internet cat1")
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("radiostart.wav")
                time.sleep(3.0)
                os.system("chromium-browser --kiosk --app=https://www.namdu1radio.com/sadbhavana-radio &")                        
                playpause = True
                cat1playpause = True
            elif not pfiles:
                print("No files to play in cat1")
                aplay("NofilesinCat1.wav")
            else:
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("Cat1.wav")
                time.sleep(0.4)
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                src_renamPath = r'/var/www/html/indexcat1.php'
                dst_renamPath = r'/var/www/html/index.php'
                shutil.copy(src_renamPath, dst_renamPath)
                os.system("chromium-browser localhost &")
                time.sleep(0.2)
                playpause = True               
            led1.off()
    ''' if button2 is pressed - Category 2 functionality button '''
    if but2.is_pressed:
        print("button2 pressed")
        previousTime = time.time()
        while but2.is_pressed:
            #Check if the button is pressed for > 2sec
            if time.time() - previousTime > 2.0:
                if((but1.is_pressed) or (but3.is_pressed) or (but4.is_pressed)or  
                (but5.is_pressed) or (but6.is_pressed) or (but7.is_pressed) or 
                (but8.is_pressed) or (but9.is_pressed) or (but10.is_pressed) or (but11.is_pressed)):
                    #if any of the buttons 2 to 9 is also pressed and held, then shutdown the Pi
                    shutdownPi()
                #if the button is pressed for more than two seconds, then longpress is True
                longpress = True
                aplay("beep_cat2.wav")
                #break
        if time.time() - previousTime < 0.1: continue
        time.sleep(0.5)
        if longpress:
            led2.on()
            os.system("killall chromium-browser")
            os.system("pkill -o chromium")
            #time.sleep(0.4)
            #os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
            #aplay("beep_cat2.wav")
            time.sleep(1.0)
            # records with 48000 quality
            arecord("recorded_audio.wav") 
            # scan for button press to stop recording
            but2.wait_for_press()
            os.system("pkill -9 arecord")
            os.system("pkill -9 aplay")
            time.sleep(0.4)
            aplay("Cat2_stop.wav")
            print("Cat2 recording stopped")
            time.sleep(5.0)
            previewplay("recorded_audio.wav")
            recFileName = "recorded@"+datetime.now().strftime('%d%b%Y_%H_%M_%S')
            # converting recorded audio to mp3 and rename with date and time of recording
            os.system("lame -b 320 "+previewaudioguidepath+"/recorded_audio.wav " +recordingpathcat2+"/"+recFileName+".mp3")
            #save the recorded audio in .upload folder respective category
            os.system("sudo cp "+recordingpathcat2+"/"+recFileName+".mp3 " +uploadpathcat2+"/"+recFileName+".mp3 &")
            os.system("pkill -9 aplay")            
            #os.system("rm "+recordingpathcat1+"/recorded_audio.wav") #remove the recorded file
            longpress = False
            cat2playpause = True
            cat2preview = True
            led2.off()
            #break
        else:
            led2.on()
            pfiles = os.listdir(uploadpathcat2)
            if cat2preview == True:
                cat2preview = False
                print("Cat2 preview stopped")
                os.system("pkill -9 aplay")
            elif cat2playpause == True:
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("radiostop.wav")
                cat2playpause = False
                playpause = False
            elif is_connected(remote_server):
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                print ("starting namma school radio from internet cat2")
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("radiostart.wav")
                time.sleep(3.0)
                os.system("chromium-browser --kiosk --app=https://www.namdu1radio.com/siddaganga-school &")                        
                playpause = True
                cat2playpause = True
            elif not pfiles:
                print("No files to play in cat2")
                aplay("NofilesinCat2.wav")
            else:
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("Cat2.wav")
                time.sleep(0.4)
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                src_renamPath = r'/var/www/html/indexcat2.php'
                dst_renamPath = r'/var/www/html/index.php'
                shutil.copy(src_renamPath, dst_renamPath)
                os.system("chromium-browser localhost &")
                time.sleep(0.2)
                playpause = True               
            led2.off()
    ''' if button3 is pressed - Category 3 functionality button '''
    if but3.is_pressed:
        print("button3 pressed")
        previousTime = time.time()
        while but3.is_pressed:
            #Check if the button is pressed for > 2sec
            if time.time() - previousTime > 2.0:
                if((but1.is_pressed) or (but2.is_pressed) or (but4.is_pressed)or  
                (but5.is_pressed) or (but6.is_pressed) or (but7.is_pressed) or 
                (but8.is_pressed) or (but9.is_pressed) or (but10.is_pressed) or (but11.is_pressed)):
                    #if any of the buttons 2 to 9 is also pressed and held, then shutdown the Pi
                    shutdownPi()
                #if the button is pressed for more than two seconds, then longpress is True
                longpress = True
                aplay("beep_cat3.wav")
                #break
        if time.time() - previousTime < 0.1: continue
        time.sleep(0.5)
        if longpress:
            #led3.on()
            os.system("killall chromium-browser")
            os.system("pkill -o chromium")
            #time.sleep(0.4)
            #os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
            #aplay("beep_cat3.wav")
            time.sleep(1.0)
            # records with 48000 quality
            arecord("recorded_audio.wav") 
            # scan for button press to stop recording
            but3.wait_for_press()
            os.system("pkill -9 arecord")
            os.system("pkill -9 aplay")
            time.sleep(0.4)
            aplay("Cat3_stop.wav")
            print("Cat3 recording stopped")
            time.sleep(5.0)
            previewplay("recorded_audio.wav")
            recFileName = "recorded@"+datetime.now().strftime('%d%b%Y_%H_%M_%S')
            # converting recorded audio to mp3 and rename with date and time of recording
            os.system("lame -b 320 "+previewaudioguidepath+"/recorded_audio.wav " +recordingpathcat3+"/"+recFileName+".mp3")
            #save the recorded audio in .upload folder respective category
            os.system("sudo cp "+recordingpathcat3+"/"+recFileName+".mp3 " +uploadpathcat3+"/"+recFileName+".mp3 &")
            os.system("pkill -9 aplay")            
            #os.system("rm "+recordingpathcat1+"/recorded_audio.wav") #remove the recorded file
            longpress = False
            cat3playpause = True
            cat3preview = True
            #led3.off()
            #break
        else:
            #led3.on()
            pfiles = os.listdir(uploadpathcat3)
            if cat3preview == True:
                cat3preview = False
                print("Cat3 preview stopped")
                os.system("pkill -9 aplay")
            elif cat3playpause == True:
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("radiostop.wav")
                cat3playpause = False
                playpause = False
            elif is_connected(remote_server):
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                print ("starting namma school radio from internet cat3")
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("radiostart.wav")
                time.sleep(3.0)
                os.system("chromium-browser --kiosk --app=https://www.namdu1radio.com/kowil-radio &")                        
                playpause = True
                cat3playpause = True
            elif not pfiles:
                print("No files to play in cat3")
                aplay("NofilesinCat3.wav")
            else:
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("Cat3.wav")
                time.sleep(0.4)
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                src_renamPath = r'/var/www/html/indexcat3.php'
                dst_renamPath = r'/var/www/html/index.php'
                shutil.copy(src_renamPath, dst_renamPath)
                os.system("chromium-browser localhost &")
                time.sleep(0.2)
                playpause = True               
            #led3.off()
    ''' if button4 is pressed - Category 4 functionality button '''
    if but4.is_pressed:
        print("button4 pressed")
        previousTime = time.time()
        while but4.is_pressed:
            #Check if the button is pressed for > 2sec
            if time.time() - previousTime > 2.0:
                if((but1.is_pressed) or (but2.is_pressed) or (but3.is_pressed)or  
                (but5.is_pressed) or (but6.is_pressed) or (but7.is_pressed) or 
                (but8.is_pressed) or (but9.is_pressed) or (but10.is_pressed) or (but11.is_pressed)):
                    #if any of the buttons 2 to 9 is also pressed and held, then shutdown the Pi
                    shutdownPi()
                #if the button is pressed for more than two seconds, then longpress is True
                longpress = True
                aplay("beep_cat4.wav")
                #break
        if time.time() - previousTime < 0.1: continue
        time.sleep(0.5)
        if longpress:
            led4.on()
            os.system("killall chromium-browser")
            os.system("pkill -o chromium")
            #time.sleep(0.4)
            #os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
            #aplay("beep_cat4.wav")
            time.sleep(1.0)
            # records with 48000 quality
            arecord("recorded_audio.wav") 
            # scan for button press to stop recording
            but4.wait_for_press()
            os.system("pkill -9 arecord")
            os.system("pkill -9 aplay")
            time.sleep(0.4)
            aplay("Cat4_stop.wav")
            print("Cat4 recording stopped")
            time.sleep(5.0)
            previewplay("recorded_audio.wav")
            recFileName = "recorded@"+datetime.now().strftime('%d%b%Y_%H_%M_%S')
            # converting recorded audio to mp3 and rename with date and time of recording
            os.system("lame -b 320 "+previewaudioguidepath+"/recorded_audio.wav " +recordingpathcat4+"/"+recFileName+".mp3")
            #save the recorded audio in .upload folder respective category
            os.system("sudo cp "+recordingpathcat4+"/"+recFileName+".mp3 " +uploadpathcat4+"/"+recFileName+".mp3 &")
            os.system("pkill -9 aplay")            
            #os.system("rm "+recordingpathcat1+"/recorded_audio.wav") #remove the recorded file
            longpress = False
            cat4playpause = True
            cat4preview = True
            led4.off()
            #break
        else:
            led4.on()
            pfiles = os.listdir(uploadpathcat4)
            if cat4preview == True:
                cat4preview = False
                print("Cat4 preview stopped")
                os.system("pkill -9 aplay")
            elif cat4playpause == True:
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("radiostop.wav")
                cat4playpause = False
                playpause = False
            elif is_connected(remote_server):
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                print ("starting namma school radio from internet cat4")
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("radiostart.wav")
                time.sleep(3.0)
                os.system("chromium-browser --kiosk --app=https://www.namdu1radio.com/budakattu-radio &")                        
                playpause = True
                cat4playpause = True
            elif not pfiles:
                print("No files to play in cat4")
                aplay("NofilesinCat4.wav")
            else:
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("Cat4.wav")
                time.sleep(0.4)
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                src_renamPath = r'/var/www/html/indexcat4.php'
                dst_renamPath = r'/var/www/html/index.php'
                shutil.copy(src_renamPath, dst_renamPath)
                os.system("chromium-browser localhost &")
                time.sleep(0.2)
                playpause = True               
            led4.off()
    ''' if button5 is pressed - Category 5 functionality button '''
    if but5.is_pressed:
        print("button5 pressed")
        previousTime = time.time()
        while but5.is_pressed:
            #Check if the button is pressed for > 2sec
            if time.time() - previousTime > 2.0:
                if((but1.is_pressed) or (but2.is_pressed) or (but3.is_pressed)or  
                (but4.is_pressed) or (but6.is_pressed) or (but7.is_pressed) or 
                (but8.is_pressed) or (but9.is_pressed) or (but10.is_pressed) or (but11.is_pressed)):
                    #if any of the buttons 2 to 9 is also pressed and held, then shutdown the Pi
                    shutdownPi()
                #if the button is pressed for more than two seconds, then longpress is True
                longpress = True
                aplay("beep_cat5.wav")
                #break
        if time.time() - previousTime < 0.1: continue
        time.sleep(0.5)
        if longpress:
            led5.on()
            os.system("killall chromium-browser")
            os.system("pkill -o chromium")
            #time.sleep(0.4)
            #os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
            #aplay("beep_cat5.wav")
            time.sleep(1.0)
            # records with 48000 quality
            arecord("recorded_audio.wav") 
            # scan for button press to stop recording
            but5.wait_for_press()
            os.system("pkill -9 arecord")
            os.system("pkill -9 aplay")
            time.sleep(0.4)
            aplay("Cat5_stop.wav")
            print("Cat5 recording stopped")
            time.sleep(5.0)
            previewplay("recorded_audio.wav")
            recFileName = "recorded@"+datetime.now().strftime('%d%b%Y_%H_%M_%S')
            # converting recorded audio to mp3 and rename with date and time of recording
            os.system("lame -b 320 "+previewaudioguidepath+"/recorded_audio.wav " +recordingpathcat5+"/"+recFileName+".mp3")
            #save the recorded audio in .upload folder respective category
            os.system("sudo cp "+recordingpathcat5+"/"+recFileName+".mp3 " +uploadpathcat5+"/"+recFileName+".mp3 &")
            os.system("pkill -9 aplay")            
            #os.system("rm "+recordingpathcat1+"/recorded_audio.wav") #remove the recorded file
            longpress = False
            cat5playpause = True
            cat5preview = True
            led5.off()
            #break
        else:
            led5.on()
            pfiles = os.listdir(uploadpathcat5)
            if cat5preview == True:
                cat5preview = False
                print("Cat5 preview stopped")
                os.system("pkill -9 aplay")
            elif cat5playpause == True:
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("radiostop.wav")
                cat5playpause = False
                playpause = False
            elif is_connected(remote_server):
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                print ("starting namma school radio from internet cat5")
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("radiostart.wav")
                time.sleep(3.0)
                os.system("chromium-browser --kiosk --app=https://www.namdu1radio.com/tvs-school-radio &")                        
                playpause = True
                cat5playpause = True
            elif not pfiles:
                print("No files to play in cat5")
                aplay("NofilesinCat5.wav")
            else:
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("Cat5.wav")
                time.sleep(0.4)
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                src_renamPath = r'/var/www/html/indexcat5.php'
                dst_renamPath = r'/var/www/html/index.php'
                shutil.copy(src_renamPath, dst_renamPath)
                os.system("chromium-browser localhost &")
                time.sleep(0.2)
                playpause = True               
            led5.off()
    ''' if button6 is pressed - Category 6 functionality button '''
    if but6.is_pressed:
        print("button6 pressed")
        previousTime = time.time()
        while but6.is_pressed:
            #Check if the button is pressed for > 2sec
            if time.time() - previousTime > 2.0:
                if((but1.is_pressed) or (but2.is_pressed) or (but3.is_pressed)or  
                (but4.is_pressed) or (but5.is_pressed) or (but7.is_pressed) or 
                (but8.is_pressed) or (but9.is_pressed) or (but10.is_pressed) or (but11.is_pressed)):
                    #if any of the buttons 2 to 9 is also pressed and held, then shutdown the Pi
                    shutdownPi()
                #if the button is pressed for more than two seconds, then longpress is True
                longpress = True
                aplay("beep_cat6.wav")
                #break
        if time.time() - previousTime < 0.1: continue
        time.sleep(0.5)
        if longpress:
            led6.on()
            os.system("killall chromium-browser")
            os.system("pkill -o chromium")
            #time.sleep(0.4)
            #os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
            #aplay("beep_cat6.wav")
            time.sleep(1.0)
            # records with 48000 quality
            arecord("recorded_audio.wav") 
            # scan for button press to stop recording
            but6.wait_for_press()
            os.system("pkill -9 arecord")
            os.system("pkill -9 aplay")
            time.sleep(0.4)
            aplay("Cat6_stop.wav")
            print("Cat6 recording stopped")
            time.sleep(5.0)
            previewplay("recorded_audio.wav")
            recFileName = "recorded@"+datetime.now().strftime('%d%b%Y_%H_%M_%S')
            # converting recorded audio to mp3 and rename with date and time of recording
            os.system("lame -b 320 "+previewaudioguidepath+"/recorded_audio.wav " +recordingpathcat6+"/"+recFileName+".mp3")
            #save the recorded audio in .upload folder respective category
            os.system("sudo cp "+recordingpathcat6+"/"+recFileName+".mp3 " +uploadpathcat6+"/"+recFileName+".mp3 &")
            os.system("pkill -9 aplay")            
            #os.system("rm "+recordingpathcat1+"/recorded_audio.wav") #remove the recorded file
            longpress = False
            cat6playpause = True
            cat6preview = True
            led6.off()
            #break
        else:
            led6.on()
            pfiles = os.listdir(uploadpathcat6)
            if cat6preview == True:
                cat6preview = False
                print("Cat6 preview stopped")
                os.system("pkill -9 aplay")
            elif cat6playpause == True:
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("radiostop.wav")
                cat6playpause = False
                playpause = False
            elif is_connected(remote_server):
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                print ("starting namma school radio from internet cat5")
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("radiostart.wav")
                time.sleep(3.0)
                os.system("chromium-browser --kiosk --app=https://www.namdu1radio.com/christ-school &")                        
                playpause = True
                cat6playpause = True
            elif not pfiles:
                print("No files to play in cat6")
                aplay("NofilesinCat6.wav")
            else:
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("Cat6.wav")
                time.sleep(0.4)
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                src_renamPath = r'/var/www/html/indexcat6.php'
                dst_renamPath = r'/var/www/html/index.php'
                shutil.copy(src_renamPath, dst_renamPath)
                os.system("chromium-browser localhost &")
                time.sleep(0.2)
                playpause = True               
            led6.off()
    ''' if button7 is pressed - Category 7 functionality button '''
    if but7.is_pressed:
        print("button7 pressed")
        previousTime = time.time()
        while but7.is_pressed:
            #Check if the button is pressed for > 2sec
            if time.time() - previousTime > 2.0:
                if((but1.is_pressed) or (but2.is_pressed) or (but3.is_pressed)or  
                (but4.is_pressed) or (but5.is_pressed) or (but6.is_pressed) or 
                (but8.is_pressed) or (but9.is_pressed) or (but10.is_pressed) or (but11.is_pressed)):
                    #if any of the buttons 2 to 9 is also pressed and held, then shutdown the Pi
                    shutdownPi()
                #if the button is pressed for more than two seconds, then longpress is True
                longpress = True
                aplay("beep_cat7.wav")
                #break
        if time.time() - previousTime < 0.1: continue
        time.sleep(0.5)
        if longpress:
            led7.on()
            os.system("killall chromium-browser")
            os.system("pkill -o chromium")
            #time.sleep(0.4)
            #os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
            #aplay("beep_cat7.wav")
            time.sleep(1.0)
            # records with 48000 quality
            arecord("recorded_audio.wav") 
            # scan for button press to stop recording
            but7.wait_for_press()
            os.system("pkill -9 arecord")
            os.system("pkill -9 aplay")
            time.sleep(0.4)
            aplay("Cat7_stop.wav")
            print("Cat7 recording stopped")
            time.sleep(4.0)
            previewplay("recorded_audio.wav")
            recFileName = "recorded@"+datetime.now().strftime('%d%b%Y_%H_%M_%S')
            # converting recorded audio to mp3 and rename with date and time of recording
            os.system("lame -b 320 "+previewaudioguidepath+"/recorded_audio.wav " +recordingpathcat7+"/"+recFileName+".mp3")
            #save the recorded audio in .upload folder respective category
            os.system("sudo cp "+recordingpathcat7+"/"+recFileName+".mp3 " +uploadpathcat7+"/"+recFileName+".mp3 &")
            os.system("pkill -9 aplay")            
            #os.system("rm "+recordingpathcat1+"/recorded_audio.wav") #remove the recorded file
            longpress = False
            cat7playpause = True
            cat7preview = True
            led7.off()
            #break
        else:
            led7.on()
            pfiles = os.listdir(uploadpathcat7)
            if cat7preview == True:
                cat7preview = False
                print("Cat7 preview stopped")
                os.system("pkill -9 aplay")
            elif cat7playpause == True:
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("radiostop.wav")
                cat7playpause = False
                playpause = False
            elif is_connected(remote_server):
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                print ("starting namma school radio from internet cat7")
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("radiostart.wav")
                time.sleep(3.0)
                os.system("chromium-browser --kiosk --app=https://www.namdu1radio.com/budakattu-radio &")                        
                playpause = True
                cat7playpause = True
            elif not pfiles:
                print("No files to play in cat7")
                aplay("NofilesinCat7.wav")
            else:
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("Cat7.wav")
                time.sleep(0.4)
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                src_renamPath = r'/var/www/html/indexcat7.php'
                dst_renamPath = r'/var/www/html/index.php'
                shutil.copy(src_renamPath, dst_renamPath)
                os.system("chromium-browser localhost &")
                time.sleep(0.2)
                playpause = True               
            led7.off()
    ''' if button8 is pressed - Category 8 functionality button '''
    if but8.is_pressed:
        print("button8 pressed")
        previousTime = time.time()
        while but8.is_pressed:
            #Check if the button is pressed for > 2sec
            if time.time() - previousTime > 2.0:
                if((but1.is_pressed) or (but2.is_pressed) or (but3.is_pressed)or  
                (but4.is_pressed) or (but5.is_pressed) or (but6.is_pressed) or 
                (but7.is_pressed) or (but9.is_pressed) or (but10.is_pressed) or (but11.is_pressed)):
                    #if any of the buttons 2 to 9 is also pressed and held, then shutdown the Pi
                    shutdownPi()
                #if the button is pressed for more than two seconds, then longpress is True
                longpress = True
                aplay("beep_cat8.wav")
                #break
        if time.time() - previousTime < 0.1: continue
        time.sleep(0.5)
        if longpress:
            led8.on()
            os.system("killall chromium-browser")
            os.system("pkill -o chromium")
            #time.sleep(0.4)
            #os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
            #aplay("beep_cat8.wav")
            time.sleep(1.0)
            # records with 48000 quality
            arecord("recorded_audio.wav") 
            # scan for button press to stop recording
            but8.wait_for_press()
            os.system("pkill -9 arecord")
            os.system("pkill -9 aplay")
            time.sleep(0.4)
            aplay("Cat8_stop.wav")
            print("Cat8 recording stopped")
            time.sleep(5.0)
            previewplay("recorded_audio.wav")
            recFileName = "recorded@"+datetime.now().strftime('%d%b%Y_%H_%M_%S')
            # converting recorded audio to mp3 and rename with date and time of recording
            os.system("lame -b 320 "+previewaudioguidepath+"/recorded_audio.wav " +recordingpathcat8+"/"+recFileName+".mp3")
            #save the recorded audio in .upload folder respective category
            os.system("sudo cp "+recordingpathcat8+"/"+recFileName+".mp3 " +uploadpathcat8+"/"+recFileName+".mp3 &")
            os.system("pkill -9 aplay")            
            #os.system("rm "+recordingpathcat1+"/recorded_audio.wav") #remove the recorded file
            longpress = False
            cat8playpause = True
            cat8preview = True
            led8.off()
            #break
        else:
            led8.on()
            pfiles = os.listdir(uploadpathcat8)
            if cat8preview == True:
                cat8preview = False
                print("Cat8 preview stopped")
                os.system("pkill -9 aplay")
            elif cat8playpause == True:
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("radiostop.wav")
                cat8playpause = False
                playpause = False
            elif is_connected(remote_server):
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                print ("starting namma school radio from internet cat8")
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("radiostart.wav")
                time.sleep(3.0)
                os.system("chromium-browser --kiosk --app=https://www.namdu1radio.com/gajanooru-radio &")                        
                playpause = True
                cat8playpause = True
            elif not pfiles:
                print("No files to play in cat8")
                aplay("NofilesinCat8.wav")
            else:
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("Cat8.wav")
                time.sleep(0.4)
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                src_renamPath = r'/var/www/html/indexcat8.php'
                dst_renamPath = r'/var/www/html/index.php'
                shutil.copy(src_renamPath, dst_renamPath)
                os.system("chromium-browser localhost &")
                time.sleep(0.2)
                playpause = True               
            led8.off()
    ''' if button9 is pressed - Category 9 functionality button '''
    if but9.is_pressed:
        print("button9 pressed")
        previousTime = time.time()
        while but9.is_pressed:
            #Check if the button is pressed for > 2sec
            if time.time() - previousTime > 2.0:
                if((but1.is_pressed) or (but2.is_pressed) or (but3.is_pressed)or  
                (but4.is_pressed) or (but5.is_pressed) or (but6.is_pressed) or 
                (but7.is_pressed) or (but8.is_pressed) or (but10.is_pressed) or (but11.is_pressed)):
                    #if any of the buttons 2 to 9 is also pressed and held, then shutdown the Pi
                    shutdownPi()
                #if the button is pressed for more than two seconds, then longpress is True
                longpress = True
                aplay("beep_cat9.wav")
                #break
        if time.time() - previousTime < 0.1: continue
        time.sleep(0.5)
        if longpress:
            led9.on()
            os.system("killall chromium-browser")
            os.system("pkill -o chromium")
            #time.sleep(0.4)
            #os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
            #aplay("beep_cat9.wav")
            time.sleep(1.0)
            # records with 48000 quality
            arecord("recorded_audio.wav") 
            # scan for button press to stop recording
            but9.wait_for_press()
            os.system("pkill -9 arecord")
            os.system("pkill -9 aplay")
            aplay("Cat9_stop.wav")
            print("Cat9 recording stopped")
            time.sleep(5.0)
            previewplay("recorded_audio.wav")
            recFileName = "recorded@"+datetime.now().strftime('%d%b%Y_%H_%M_%S')
            # converting recorded audio to mp3 and rename with date and time of recording
            os.system("lame -b 320 "+previewaudioguidepath+"/recorded_audio.wav " +recordingpathcat9+"/"+recFileName+".mp3")
            #save the recorded audio in .upload folder respective category
            os.system("sudo cp "+recordingpathcat9+"/"+recFileName+".mp3 " +uploadpathcat9+"/"+recFileName+".mp3 &")
            os.system("pkill -9 aplay")            
            #os.system("rm "+recordingpathcat1+"/recorded_audio.wav") #remove the recorded file
            longpress = False
            cat9playpause = True
            cat9preview = True
            led9.off()
            #break
        else:
            led9.on()
            pfiles = os.listdir(uploadpathcat9)
            if cat9preview == True:
                cat9preview = False
                print("Cat9 preview stopped")
                os.system("pkill -9 aplay")
            elif cat9playpause == True:
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("radiostop.wav")
                cat9playpause = False
                playpause = False
            elif is_connected(remote_server):
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                print ("starting namma school radio from internet cat9")
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("radiostart.wav")
                time.sleep(3.0)
                os.system("chromium-browser --kiosk --app=https://www.namdu1radio.com/dhamma-chitra-durga &")                        
                playpause = True
                cat9playpause = True
            elif not pfiles:
                print("No files to play in cat9")
                aplay("NofilesinCat9.wav")
            else:
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("Cat9.wav")
                time.sleep(0.4)
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                src_renamPath = r'/var/www/html/indexcat9.php'
                dst_renamPath = r'/var/www/html/index.php'
                shutil.copy(src_renamPath, dst_renamPath)
                os.system("chromium-browser localhost &")
                time.sleep(0.2)
                playpause = True               
            led9.off()
    ''' if button10 is pressed - Category 10 functionality button '''
    if but10.is_pressed:
        print("button10 pressed")
        previousTime = time.time()
        while but10.is_pressed:
            #Check if the button is pressed for > 2sec
            if time.time() - previousTime > 2.0:
                if((but1.is_pressed) or (but2.is_pressed) or (but3.is_pressed)or  
                (but4.is_pressed) or (but5.is_pressed) or (but6.is_pressed) or 
                (but7.is_pressed) or (but8.is_pressed) or (but9.is_pressed) or (but11.is_pressed)):
                    #if any of the buttons 2 to 9 is also pressed and held, then shutdown the Pi
                    shutdownPi()
                #if the button is pressed for more than two seconds, then longpress is True
                longpress = True
                aplay("beep_cat10.wav")
                #break
        if time.time() - previousTime < 0.1: continue
        time.sleep(0.5)
        if longpress:
            led10.on()
            os.system("killall chromium-browser")
            os.system("pkill -o chromium")
            #os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
            #aplay("beep_cat10.wav")
            time.sleep(1.0)
            # records with 48000 quality
            arecord("recorded_audio.wav") 
            # scan for button press to stop recording
            but10.wait_for_press()
            os.system("pkill -9 arecord")
            os.system("pkill -9 aplay")
            time.sleep(0.4)
            aplay("Cat10_stop.wav")
            print("Cat10 recording stopped")
            time.sleep(5.0)
            previewplay("recorded_audio.wav")
            recFileName = "recorded@"+datetime.now().strftime('%d%b%Y_%H_%M_%S')
            # converting recorded audio to mp3 and rename with date and time of recording
            os.system("lame -b 320 "+previewaudioguidepath+"/recorded_audio.wav " +recordingpathcat10+"/"+recFileName+".mp3")
            #save the recorded audio in .upload folder respective category
            os.system("sudo cp "+recordingpathcat10+"/"+recFileName+".mp3 " +uploadpathcat10+"/"+recFileName+".mp3 &")
            os.system("pkill -9 aplay")            
            #os.system("rm "+recordingpathcat1+"/recorded_audio.wav") #remove the recorded file
            longpress = False
            cat10playpause = True
            cat10preview = True
            led10.off()
            #break
        else:
            led10.on()
            pfiles = os.listdir(uploadpathcat10)
            if cat10preview == True:
                cat10preview = False
                print("Cat10 preview stopped")
                os.system("pkill -9 aplay")
            elif cat10playpause == True:
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("radiostop.wav")
                cat10playpause = False
                playpause = False
            elif is_connected(remote_server):
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                print ("starting namma school radio from internet cat10")
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("radiostart.wav")
                time.sleep(3.0)
                os.system("chromium-browser --kiosk --app=https://www.namdu1radio.com/thanmayi-school-radio &")                        
                playpause = True
                cat10playpause = True
            elif not pfiles:
                print("No files to play in cat10")
                aplay("NofilesinCat10.wav")
            else:
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay("Cat10.wav")
                time.sleep(0.4)
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                src_renamPath = r'/var/www/html/indexcat10.php'
                dst_renamPath = r'/var/www/html/index.php'
                shutil.copy(src_renamPath, dst_renamPath)
                os.system("chromium-browser localhost &")
                time.sleep(0.2)
                playpause = True               
            led10.off()   
    '''upload and backup play functionality'''
    if but11.is_pressed:
        #os.system("killall chromium-browser")
        #os.system("pkill -o chromium")
        print("buttons 11 pressed")
        previousTime = time.time()
        while but11.is_pressed:
            #Check if the button is pressed for > 2sec
            if time.time() - previousTime > 2.0:
                if but1.is_pressed or but2.is_pressed or but3.is_pressed \
                or but4.is_pressed or but5.is_pressed or but6.is_pressed \
                or but7.is_pressed or but8.is_pressed or but9.is_pressed \
                or but10.is_pressed :
                    #if any of the buttons 1 to 9 is also pressed and held, then shutdown the Pi
                    shutdownPi()
                # if the button is pressed for more than two seconds, then longpress is True
                longpress = True
                #break
                aplay("beep_catgen.wav")
                # if longpress is True, record audio after a 'beep'
        if time.time() - previousTime < 0.1: continue
        time.sleep(0.5)
        if longpress:
            led.fwd_blink("slow")
            os.system("killall chromium-browser")
            os.system("pkill -o chromium")
            #os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
            print("Gencat recording started")
            #aplay("beep_catgen.wav")
            #time.sleep(1.0)
            recFileName = "recorded@"+datetime.now().strftime('%d%b%Y_%H_%M_%S')
            # records with 48000 quality
            arecord(previewaudioguidepath, recFileName+".wav")
            # scan for button press to stop recording
            but11.wait_for_press()
            os.system("pkill -9 arecord")
            os.system("pkill -9 aplay")
            aplay("Catgen_stop.wav")
            #time.sleep(1.4)
            print("Gencat recording stopped")
            #time.sleep(5.0)
            previewplay(recordingpathcat11, recFileName+".wav")
            os.system("cp "+previewaudioguidepath+"/"+recFileName+".wav " +recordingpathcat11+"/"+recFileName+".wav")
            os.system("lxterminal -e python "+projectpath+"/Wav2Mp3Convert.py  &")
            os.system("rm "+previewaudioguidepath+"/"+recFileName+".wav")
            led.fwd_on()
            longpress = False
            gencatpreview = True
        else:
            if gencatpreview == True:
                gencatpreview = False
                print("Gen cat preview stopped")
                os.system("pkill -9 aplay")
            elif playpause == True:
                playpause = False
                print ("echo closing radio !!!")
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                os.system("pkill -9 aplay")
                time.sleep(0.2)
                aplay("radiostop.wav")
                #break
            #Check whether the local server is connected    
            elif is_onradio() and is_connected(local_server):
                os.system("pkill -9 aplay")
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                print ("starting namma school radio....from local server ")
                time.sleep(0.4)
                aplay("radiostart.wav")
                time.sleep(0.4)
                os.system("chromium-browser --kiosk --app=http://"+local_server+" &")
                playpause = True
            # Check whether the internet is available to play from the website
            elif is_connected(remote_server):
                print ("starting namma school radio from internet")
                os.system("pkill -9 aplay")
                os.system("pkill -o chromium")
                os.system("killall chromium-browser")
                aplay("radiostart.wav")
                os.system("chromium-browser --kiosk --app=http://stream.zeno.fm/ghuhx13nf5zuv &") 
                time.sleep(0.4)                        
                playpause = True
            else:
                print ("Button11 general playback started")
                os.system("pkill -9 aplay")
                os.system("pkill -o chromium")
                aplay("radiostart.wav")
                src_renamPath = r'/var/www/html/indexgencat.php'
                dst_renamPath = r'/var/www/html/index.php'
                shutil.copy(src_renamPath, dst_renamPath)
                #Starts playing mp3 from .upload folder
                os.system("chromium-browser --kiosk localhost &")
                time.sleep(0.2)
                playpause = True
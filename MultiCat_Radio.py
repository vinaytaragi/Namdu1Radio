#!/usr/bin/python
# @brief: Script to record and upload the audio files
#         GPIO's are used for recoplaypauserding and uploading
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


# *** Global Variables *** #
previousTime = False
but1n2_pressed = False
var = "Hello"
radio = False
duration = 5
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
# network verification variables
remote_server = "www.google.com"
local_server = "192.168.1.50"
 

# setting folder paths
projectpath =  os.path.split(os.path.realpath(__file__))[0]
audioguidepath = projectpath + "/audio-alert"
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
    os.system("aplay -D plughw:CARD=0,DEV=0 "+audioguidepath+"/"+filename)

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
    Function to get the name of the pendrive connected
'''    
def getDevName():
    '''The below code to identify the pendrive folder name - Start'''
    os.system('rm -rf /home/pi/Documents/Namdu1Radio/usbs1.txt')
    os.system('ls /media/pi > /home/pi/Documents/Namdu1Radio/usbs1.txt')
    file1 = open("/home/pi/Documents/Namdu1Radio/usbs1.txt", "r")
    Lines = file1.readlines()
    # Strips the newline character
    for line in Lines:
        line = line.rstrip("\n")
        if (line == '7022-5CC71'):
            penDet = False
            var = line
            #print(line)
            #break;
        elif (line == '7022-5CC72'):
            penDet = False
            var = line
            #print(line)
            #break;
        elif (line == '7022-5CC7'):
            penDet = False
            var = line
            #print(line)
        else:
            var = line
            penDet = True
            print("Pendrive name:",var)
    return var

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
led3 = LED(24) #GPIO24 - LED3
led4 = LED(25) #GPIO25 - LED4
led5 = LED(8)  #GPIO8  - LED5
led6 = LED(7)  #GPIO7  - LED6
led7 = LED(12) #GPIO12 - LED7
led8 = LED(16) #GPIO16 - LED8
led9 = LED(20) #GPIO20 - LED9

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

# *** Setting up GPIO of Pi *** #
GPIO.setmode(GPIO.BCM)

#Pi started indication audio
print("pi Started")
os.system("aplay -D plughw:CARD=0,DEV=0 "+audioguidepath+"/lappiready.wav &")
aplay("lappiready.wav")
time.sleep(0.5)

while True:
    print("pi Running")
    #Check whether local server connected
    if is_onradio() and is_connected(local_server) and cntr:
        os.system("pkill -9 aplay")
        time.sleep(0.1)
        print ("starting namma school radio....from local server ")
        aplay("radiostart.wav")
        time.sleep(5)
        os.system("chromium-browser --app=http://"+local_server+" &")        
        cntr = False
        playpause = True
    #Check whether the internet is available to play from the website
    elif is_connected(remote_server) and cntr:
        print ("starting namma school radio from internet")
        os.system("pkill -9 aplay")
        aplay("radiostart.wav")
        time.sleep(5)
        os.system("chromium-browser --app=https://www.namdu1radio.com/sadbhavana-radio &")
        cntr = False
        playpause = True
    elif cntr == True:
        print ("Local and remote server not available")
        print ("Audio starts from localhost")
        os.system("pkill -9 aplay")
        src_renamPath = r'/var/www/html/index_original.php'
        dst_renamPath = r'/var/www/html/index.php'
        shutil.copy(src_renamPath, dst_renamPath)
        aplay("radiostart.wav")
        time.sleep(10)
        os.system("chromium-browser localhost &")
        cntr = False
        playpause = True
        time.sleep(0.2)
        
    #pendrive name
    devname =  getDevName()
    #destination path  
    destpath1 = r"/media/pi/"+devname+r"/cat"
    if penDet == True:    
        rv1 = subprocess.call("grep -qs '/media/pi' /proc/mounts", shell=True)
        rv2 = subprocess.call("mount | grep /media/pi", shell=True)
        penDet = False
    ''' if button1 is pressed - Category 1 functionality button '''
    if but1.is_pressed:
        print("button1 pressed")
        os.system("killall chromium-browser")
        previousTime = time.time()
        while but1.is_pressed:
            #Check if the button is pressed for > 2sec
            if time.time() - previousTime > 2.0:
                if((but2.is_pressed) or (but3.is_pressed) or (but4.is_pressed)or  
                (but5.is_pressed) or (but6.is_pressed) or (but7.is_pressed) or 
                (but8.is_pressed) or (but9.is_pressed)):
                    #if any of the buttons 2 to 9 is also pressed and held, then shutdown the Pi
                    shutdownPi()
                #if the button is pressed for more than two seconds, then longpress is True
                longpress = True
                time.sleep(0.5)
                if longpress:
                    led1.on()
                    os.system("killall chromium-browser")
                    time.sleep(0.4)
                    os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
                    aplay("beep_cat1.wav")
                    # records with 48000 quality
                    os.system("arecord "+recordingpathcat1+"/recorded_audio.wav -D sysdefault:CARD=1 -f dat & ") 
                    # scan for button press to stop recording
                    but1.wait_for_press()
                    os.system("pkill -9 arecord")
                    os.system("pkill -9 aplay")
                    aplay("Cat1_stop.wav")
                    os.system("lame -b 320 "+recordingpathcat1+"/recorded_audio.wav "+recordingpathcat1+"/recorded@"+datetime.now().strftime('%d%b%Y_%H:%M')+".mp3 &")
                    os.system("rm "+recordingpathcat1) #remove the recorded file
                    longpress = False
                    led1.off()
                    break
            else:
                #led1.on()
                os.system("pkill -9 aplay")
                #Get the list files in .upload/cat1 folder
                pfiles = os.listdir(uploadpathcat1)
                if not pfiles:
                    print("No files to play in cat1")
                    aplay("NofilesinCat1.wav")
                else:
                    if is_connected(remote_server):
                        os.system("killall chromium-browser")
                        print ("starting namma school radio from internet cat1")
                        os.system("pkill -9 aplay")
                        aplay("radiostart.wav")
                        time.sleep(0.5)
                        os.system("chromium-browser --app=https://www.namdu1radio.com/sadbhavana-radio &")                        
                        playpause = True
                    else:
                        os.system("pkill -9 aplay")
                        time.sleep(0.4)
                        aplay("Cat1.wav")
                        time.sleep(0.4)
                        os.system("killall chromium-browser")
                        src_renamPath = r'/var/www/html/indexcat1.php'
                        dst_renamPath = r'/var/www/html/index.php'
                        shutil.copy(src_renamPath, dst_renamPath)
                        os.system("chromium-browser localhost &")
                        time.sleep(0.2)
                        playpause = True               
                #led1.off()            
    ''' if button2 is pressed - Category 2 functionality button '''
    if but2.is_pressed:
        print("button2 pressed")
        os.system("killall chromium-browser")
        previousTime = time.time()
        while but2.is_pressed:
            print("button2 while entered ")
            #Check if the button is pressed for > 2sec
            if time.time() - previousTime > 2.0:
                if ((but1.is_pressed) or (but3.is_pressed) or (but4.is_pressed) or
                (but5.is_pressed) or (but6.is_pressed) or (but7.is_pressed) or
                (but8.is_pressed) or (but9.is_pressed)):
                    #if any of the buttons 2 to 9 is also pressed and held, then shutdown the Pi
                    shutdownPi()
                # if the button is pressed for more than two seconds, then longpress is True
                print("button2 long press")
                longpress = True
                time.sleep(0.5)
                if longpress:
                    print("button2 start recording")
                    os.system("killall chromium-browser")
                    time.sleep(0.4)
                    led2.on()
                    os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
                    aplay("beep_cat2.wav")
                    # records with 48000 quality
                    os.system("arecord "+recordingpathcat2+"/recorded_audio.wav -D sysdefault:CARD=1 -f dat & ") 
                    # scan for button press to stop recording
                    but2.wait_for_press()
                    os.system("pkill -9 arecord")
                    os.system("pkill -9 aplay")
                    aplay("Cat2_stop.wav")
                    print("button2 stopped recording")
                    # converting recorded audio to mp3 and rename with date and time of recording
                    os.system("lame -b 320 "+recordingpathcat2+"/recorded_audio.wav "+recordingpathcat2+"/recorded@"+datetime.now().strftime('%d%b%Y_%H:%M')+".mp3 &")
                    os.system("rm "+recordingpathcat2)#remove the recorded file
                    longpress = False
                    led2.off()
                    break
            else:
                #led2.on()
                os.system("pkill -9 aplay")
                #Get the list files in .upload/cat1 folder
                pfiles = os.listdir(uploadpathcat2)
                if not pfiles:
                    print("No files to play in cat2")
                    aplay("NofilesinCat2.wav")
                else:
                    if is_connected(remote_server):
                        os.system("killall chromium-browser")
                        print ("starting namma school radio from internet t cat2")
                        os.system("pkill -9 aplay")
                        aplay("radiostart.wav")
                        time.sleep(0.5)
                        os.system("chromium-browser --app=https://www.namdu1radio.com/siddaganga-school &")                        
                        playpause = True
                    else:
                        os.system("pkill -9 aplay")
                        time.sleep(0.4)
                        aplay("Cat2.wav")
                        time.sleep(0.4)
                        os.system("pkill -o chromium")
                        os.system("killall chromium-browser")
                        src_renamPath = r'/var/www/html/indexcat2.php'
                        dst_renamPath = r'/var/www/html/index.php'
                        shutil.copy(src_renamPath, dst_renamPath)
                        os.system("chromium-browser localhost &")
                        time.sleep(0.2)
                        playpause = True
                #led2.off()            
    ''' if button3 is pressed - Category 3 functionality button '''
    if but3.is_pressed:
        print("button3 pressed")
        os.system("killall chromium-browser")
        previousTime = time.time()
        while but3.is_pressed:
            #Check if the button is pressed for > 2sec
            if time.time() - previousTime > 2.0:
                if ((but1.is_pressed) or (but2.is_pressed) or (but4.is_pressed) or
                (but5.is_pressed) or (but6.is_pressed) or (but7.is_pressed) or
                (but8.is_pressed) or (but9.is_pressed)):
                    #if any of the buttons 2 to 9 is also pressed and held, then shutdown the Pi
                    shutdownPi()
                # if the button is pressed for more than two seconds, then longpress is True
                longpress = True
                time.sleep(0.5)
                if longpress:
                    os.system("killall chromium-browser")
                    time.sleep(0.4)
                    led3.on()
                    os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
                    aplay("beep_cat3.wav")
                    # records with 48000 quality
                    os.system("arecord "+recordingpathcat3+"/recorded_audio.wav -D sysdefault:CARD=1 -f dat & ") 
                    # scan for button press to stop recording
                    but3.wait_for_press()
                    os.system("pkill -9 arecord")
                    aplay("Cat3_stop.wav")
                    # converting recorded audio to mp3 and rename with date and time of recording
                    os.system("lame -b 320 "+recordingpathcat3+"/recorded_audio.wav "+recordingpathcat3+"/recorded@"+datetime.now().strftime('%d%b%Y_%H:%M')+".mp3 &")
                    os.system("rm "+recordingpathcat3)#remove the recorded file
                    longpress = False
                    led3.off()
                    break
            else:
                #led3.on()
                os.system("pkill -9 aplay")
                #Get the list files in .upload/cat1 folder
                pfiles = os.listdir(uploadpathcat3)
                if not pfiles:
                    print("No files to play in cat3")
                    aplay("NofilesinCat3.wav")
                else:
                    if is_connected(remote_server):
                        os.system("killall chromium-browser")
                        print ("starting namma school radio from internet t cat3")
                        os.system("pkill -9 aplay")
                        aplay("radiostart.wav")
                        time.sleep(0.5)
                        os.system("chromium-browser --app=https://www.namdu1radio.com/kowil-radio &")                        
                        playpause = True
                    else:
                        os.system("pkill -9 aplay")
                        time.sleep(0.4)
                        aplay("Cat3.wav &")
                        time.sleep(0.4)
                        os.system("pkill -o chromium")
                        os.system("killall chromium-browser")
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
        os.system("killall chromium-browser")
        previousTime = time.time()
        while but4.is_pressed:
            #Check if the button is pressed for > 2sec
            if time.time() - previousTime > 2.0:
                if ((but1.is_pressed) or (but2.is_pressed) or (but3.is_pressed) or
                (but5.is_pressed) or (but6.is_pressed) or (but7.is_pressed) or
                (but8.is_pressed) or (but9.is_pressed)):
                    #if any of the buttons 2 to 9 is also pressed and held, then shutdown the Pi
                    shutdownPi()
                # if the button is pressed for more than two seconds, then longpress is True
                longpress = True
                time.sleep(0.5)
                if longpress:
                    led4.on()
                    os.system("killall chromium-browser")
                    time.sleep(0.4)
                    os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
                    aplay("beep_cat4.wav")
                    # records with 48000 quality
                    os.system("arecord "+recordingpathcat4+"/recorded_audio.wav -D sysdefault:CARD=1 -f dat & ") 
                    # scan for button press to stop recording
                    but4.wait_for_press()
                    os.system("pkill -9 arecord")
                    aplay("Cat4_stop.wav")
                    # converting recorded audio to mp3 and rename with date and time of recording
                    os.system("lame -b 320 "+recordingpathcat4+"/recorded_audio.wav "+recordingpathcat4+"/recorded@"+datetime.now().strftime('%d%b%Y_%H:%M')+".mp3 &")
                    os.system("rm "+recordingpathcat4)#remove the recorded file
                    longpress = False
                    led4.off()
                    break
            else:
                #led4.on()
                os.system("pkill -9 aplay")
                #Get the list files in .upload/cat1 folder
                pfiles = os.listdir(uploadpathcat4)
                if not pfiles:
                    print("No files to play in cat4")
                    aplay("NofilesinCat4.wav")
                else:
                    if is_connected(remote_server):
                        os.system("killall chromium-browser")
                        print ("starting namma school radio from internet t cat4")
                        os.system("pkill -9 aplay")
                        aplay("radiostart.wav")
                        time.sleep(0.5)
                        os.system("chromium-browser --app=https://www.namdu1radio.com/budakattu-radio &")                        
                        playpause = True
                    else:
                        os.system("pkill -9 aplay")
                        time.sleep(0.4)
                        aplay("Cat4.wav")
                        time.sleep(0.4)
                        os.system("pkill -o chromium")
                        os.system("killall chromium-browser")
                        src_renamPath = r'/var/www/html/indexcat4.php'
                        dst_renamPath = r'/var/www/html/index.php'
                        shutil.copy(src_renamPath, dst_renamPath)
                        os.system("chromium-browser localhost &")
                        time.sleep(0.2)
                        playpause = True
                #led4.off()            
    ''' if button5 is pressed - Category 5 functionality button '''
    if but5.is_pressed:
        print("button5 pressed")
        os.system("killall chromium-browser")
        previousTime = time.time()
        #but5.wait_for_release()
        while but5.is_pressed:
            #Check if the button is pressed for > 2sec
            if time.time() - previousTime > 2.0:
                if but1.is_pressed or but2.is_pressed or but3.is_pressed \
                or but4.is_pressed or but6.is_pressed or but7.is_pressed \
                or but8.is_pressed or but9.is_pressed :
                    #if any of the buttons 2 to 9 is also pressed and held, then shutdown the Pi
                    shutdownPi()
                # if the button is pressed for more than two seconds, then longpress is True
                longpress = True
                time.sleep(0.5)
                if longpress:
                    led5.on()
                    os.system("killall chromium-browser")
                    time.sleep(0.4)
                    os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
                    aplay("beep_cat5.wav")
                    # records with 48000 quality
                    os.system("arecord "+recordingpathcat5+"/recorded_audio.wav -D sysdefault:CARD=1 -f dat & ") 
                    # scan for button press to stop recording
                    but5.wait_for_press()
                    os.system("pkill -9 arecord")
                    aplay("Cat5_stop.wav")
                    # converting recorded audio to mp3 and rename with date and time of recording
                    os.system("lame -b 320 "+recordingpathcat5+"/recorded_audio.wav "+recordingpathcat5+"/recorded@"+datetime.now().strftime('%d%b%Y_%H:%M')+".mp3 &")
                    os.system("rm "+recordingpathcat5)#remove the recorded file
                    longpress = False
                    led5.off()
                    break
            else:
                #led5.on()
                os.system("pkill -9 aplay")
                #Get the list files in .upload/cat1 folder
                pfiles = os.listdir(uploadpathcat5)
                if not pfiles:
                    print("No files to play in cat5")
                    aplay("NofilesinCat1.wav")
                else:
                    if is_connected(remote_server):
                        os.system("killall chromium-browser")
                        print ("starting namma school radio from internet t cat5")
                        os.system("pkill -9 aplay")
                        aplay("radiostart.wav")
                        time.sleep(0.5)
                        os.system("chromium-browser --app=https://www.namdu1radio.com/tvs-school-radio &")                        
                        playpause = True
                    else:
                        os.system("pkill -9 aplay")
                        time.sleep(0.4)
                        aplay("Cat5.wav")
                        time.sleep(0.4)
                        os.system("pkill -o chromium")
                        os.system("killall chromium-browser")
                        src_renamPath = r'/var/www/html/indexcat5.php'
                        dst_renamPath = r'/var/www/html/index.php'
                        shutil.copy(src_renamPath, dst_renamPath)
                        os.system("chromium-browser localhost &")
                        time.sleep(0.2)
                        playpause = True
                #led5.off()            
    ''' if button6 is pressed - Category 6 functionality button '''
    if but6.is_pressed:
        print("button6 pressed")
        os.system("killall chromium-browser")
        previousTime = time.time()
        #but6.wait_for_release()
        while but6.is_pressed:
            #Check if the button is pressed for > 2sec
            if time.time() - previousTime > 2.0:
                if but1.is_pressed or but2.is_pressed or but3.is_pressed \
                or but4.is_pressed or but5.is_pressed or but7.is_pressed \
                or but8.is_pressed or but9.is_pressed :
                    #if any of the buttons 2 to 9 is also pressed and held, then shutdown the Pi
                    shutdownPi()
                # if the button is pressed for more than two seconds, then longpress is True
                longpress = True
                time.sleep(0.5)
                if longpress:
                    led6.on()
                    os.system("killall chromium-browser")
                    time.sleep(0.4)
                    os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
                    aplay("beep_cat6.wav")
                    # records with 48000 quality
                    os.system("arecord "+recordingpathcat6+"/recorded_audio.wav -D sysdefault:CARD=1 -f dat & ") 
                    # scan for button press to stop recording
                    but6.wait_for_press()
                    os.system("pkill -9 arecord")
                    aplay("Cat6_stop.wav")
                    # converting recorded audio to mp3 and rename with date and time of recording
                    os.system("lame -b 320 "+recordingpathcat6+"/recorded_audio.wav "+recordingpathcat6+"/recorded@"+datetime.now().strftime('%d%b%Y_%H:%M')+".mp3 &")
                    #os.system("rm "+recordingpathcat6)#remove the recorded file
                    longpress = False
                    led6.off()
                    break
            else:
                #led6.on()
                os.system("pkill -9 aplay")
                #Get the list files in .upload/cat1 folder
                pfiles = os.listdir(uploadpathcat6)
                if not pfiles:
                    print("No files to play in cat6")
                    os.system("pkill -9 aplay")
                    aplay("NofilesinCat6.wav")
                else:
                    if is_connected(remote_server):
                        os.system("killall chromium-browser")
                        print ("starting namma school radio from internet t cat6")
                        os.system("pkill -9 aplay")
                        aplay("radiostart.wav")
                        time.sleep(0.5)
                        os.system("chromium-browser --app=https://www.namdu1radio.com/christ-school &")                        
                        playpause = True
                    else:
                        os.system("pkill -9 aplay")
                        time.sleep(0.4)
                        aplay("Cat6.wav")
                        time.sleep(0.4)
                        os.system("pkill -o chromium")
                        os.system("killall chromium-browser")
                        src_renamPath = r'/var/www/html/indexcat6.php'
                        dst_renamPath = r'/var/www/html/index.php'
                        shutil.copy(src_renamPath, dst_renamPath)
                        os.system("chromium-browser localhost &")
                        time.sleep(0.2)
                        playpause = True
                #led6.off()            
    ''' if button7 is pressed - Category 7 functionality button '''
    if but7.is_pressed:
        print("button7 pressed")
        previousTime = time.time()
        #but7.wait_for_release()
        while but7.is_pressed:
            #Check if the button is pressed for > 2sec
            if time.time() - previousTime > 2.0:
                if ((but1.is_pressed) or (but2.is_pressed) or (but3.is_pressed) or
                (but4.is_pressed) or (but5.is_pressed) or (but6.is_pressed) or
                (but8.is_pressed) or (but9.is_pressed)):
                    #if any of the buttons 2 to 9 is also pressed and held, then shutdown the Pi
                    shutdownPi()
                # if the button is pressed for more than two seconds, then longpress is True
                longpress = True
                time.sleep(0.5)
                if longpress:
                    led7.on()
                    os.system("killall chromium-browser")
                    time.sleep(0.4)
                    os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
                    aplay("beep_cat7.wav")
                    # records with 48000 quality
                    os.system("arecord "+recordingpathcat7+"/recorded_audio.wav -D sysdefault:CARD=1 -f dat & ") 
                    # scan for button press to stop recording
                    but7.wait_for_press()
                    os.system("pkill -9 arecord")
                    aplay("Cat7_stop.wav")
                    # converting recorded audio to mp3 and rename with date and time of recording
                    os.system("lame -b 320 "+recordingpathcat7+"/recorded_audio.wav "+recordingpathcat7+"/recorded@"+datetime.now().strftime('%d%b%Y_%H:%M')+".mp3 &")
                    os.system("rm "+recordingpathcat7)#remove the recorded file
                    longpress = False
                    led7.off()
                    break
            else:
                #led7.on()
                os.system("pkill -9 aplay")
                #Get the list files in .upload/cat1 folder
                pfiles = os.listdir(uploadpathcat7)
                if not pfiles:
                    print("No files to play in cat7")
                    os.system("pkill -9 aplay")
                    aplay("NofilesinCat7.wav")
                else:
                    if is_connected(remote_server):
                        os.system("killall chromium-browser")
                        print ("starting namma school radio from internet t cat7")
                        os.system("pkill -9 aplay")
                        aplay("radiostart.wav")
                        time.sleep(0.5)
                        os.system("chromium-browser --app=https://www.namdu1radio.com/budakattu-radio &")                        
                        playpause = True
                    else:
                        os.system("pkill -9 aplay")
                        time.sleep(0.4)
                        aplay("Cat7.wav")
                        time.sleep(0.4)
                        os.system("pkill -o chromium")
                        os.system("killall chromium-browser")
                        src_renamPath = r'/var/www/html/indexcat7.php'
                        dst_renamPath = r'/var/www/html/index.php'
                        shutil.copy(src_renamPath, dst_renamPath)
                        os.system("chromium-browser localhost &")
                        time.sleep(0.2)
                        playpause = True
                #led7.off()            
    ''' if button8 is pressed - Category 8 functionality button '''
    if but8.is_pressed:
        print("button8 pressed")
        os.system("killall chromium-browser")
        previousTime = time.time()
        #but8.wait_for_release()
        while but8.is_pressed:
            #Check if the button is pressed for > 2sec
            if time.time() - previousTime > 2.0:
                if but1.is_pressed or but2.is_pressed or but3.is_pressed \
                or but4.is_pressed or but5.is_pressed or but6.is_pressed \
                or but7.is_pressed or but9.is_pressed :
                    #if any of the buttons 2 to 9 is also pressed and held, then shutdown the Pi
                    shutdownPi()
                # if the button is pressed for more than two seconds, then longpress is True
                longpress = True
                time.sleep(0.5)
                if longpress:
                    led8.on()
                    os.system("killall chromium-browser")
                    time.sleep(0.4)
                    os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
                    aplay("beep_cat8.wav")
                    # records with 48000 quality
                    os.system("arecord "+recordingpathcat8+"/recorded_audio.wav -D sysdefault:CARD=1 -f dat & ") 
                    # scan for button press to stop recording
                    but8.wait_for_press()
                    os.system("pkill -9 arecord")
                    aplay("Cat8_stop.wav")
                    # converting recorded audio to mp3 and rename with date and time of recording
                    os.system("lame -b 320 "+recordingpathcat8+"/recorded_audio.wav "+recordingpathcat8+"/recorded@"+datetime.now().strftime('%d%b%Y_%H:%M')+".mp3 &")
                    os.system("rm "+recordingpathcat8)#remove the recorded file
                    longpress = False
                    led8.off()
                    break
            else:
                #led8.on()
                os.system("pkill -9 aplay")
                #Get the list files in .upload/cat1 folder
                pfiles = os.listdir(uploadpathcat8)
                if not pfiles:
                    print("No files to play in cat8")
                    os.system("pkill -9 aplay")
                    aplay("NofilesinCat8.wav")
                else:
                    if is_connected(remote_server):
                        os.system("killall chromium-browser")
                        print ("starting namma school radio from internet t cat8")
                        os.system("pkill -9 aplay")
                        aplay("radiostart.wav")
                        time.sleep(0.5)
                        os.system("chromium-browser --app=https://www.namdu1radio.com/gajanooru-radio &")                        
                        playpause = True
                    else:
                        os.system("pkill -9 aplay")
                        time.sleep(0.4)
                        aplay("Cat8.wav")
                        time.sleep(0.4)
                        os.system("pkill -o chromium")
                        os.system("killall chromium-browser")
                        src_renamPath = r'/var/www/html/indexcat8.php'
                        dst_renamPath = r'/var/www/html/index.php'
                        shutil.copy(src_renamPath, dst_renamPath)
                        os.system("chromium-browser localhost &")
                        time.sleep(0.2)
                        playpause = True
                #led8.off()
    ''' if button9 is pressed - Category 8 functionality button '''
    if but9.is_pressed:        
        print("button9 pressed")
        os.system("killall chromium-browser")
        previousTime = time.time()
        #but8.wait_for_release()
        while but9.is_pressed:
            #Check if the button is pressed for > 2sec
            if time.time() - previousTime > 2.0:
                if but1.is_pressed or but2.is_pressed or but3.is_pressed \
                or but4.is_pressed or but5.is_pressed or but6.is_pressed \
                or but7.is_pressed or but8.is_pressed :
                    #if any of the buttons 2 to 9 is also pressed and held, then shutdown the Pi
                    shutdownPi()
                # if the button is pressed for more than two seconds, then longpress is True
                longpress = True
                time.sleep(0.5)
                if longpress:
                    led9.on()
                    os.system("killall chromium-browser")
                    time.sleep(0.4)
                    os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
                    aplay("beep_cat9.wav")
                    # records with 48000 quality
                    os.system("arecord "+recordingpathcat9+"/recorded_audio.wav -D sysdefault:CARD=1 -f dat & ") 
                    # scan for button press to stop recording
                    but9.wait_for_press()
                    os.system("pkill -9 arecord")
                    aplay("Cat9_stop.wav")
                    # converting recorded audio to mp3 and rename with date and time of recording
                    os.system("lame -b 320 "+recordingpathcat9+"/recorded_audio.wav "+recordingpathcat9+"/recorded@"+datetime.now().strftime('%d%b%Y_%H:%M')+".mp3 &")
                    os.system("rm "+recordingpathcat9)#remove the recorded file
                    longpress = False
                    led9.off()
                    break
            else:
                #led9.on()
                os.system("pkill -9 aplay")
                #Get the list files in .upload/cat1 folder
                pfiles = os.listdir(uploadpathcat1)
                if not pfiles:
                    print("No files to play in cat9")
                    aplay("NofilesinCat9.wav")
                else:
                    if is_connected(remote_server):
                        os.system("killall chromium-browser")
                        print ("starting namma school radio from internet t cat9")
                        os.system("pkill -9 aplay")
                        aplay("radiostart.wav")
                        time.sleep(0.5)
                        os.system("chromium-browser --app=https://www.namdu1radio.com/dhamma-chitra-durga &")                        
                        playpause = True
                    else:
                        os.system("pkill -9 aplay")
                        time.sleep(0.4)
                        aplay("Cat9.wav")
                        time.sleep(0.4)
                        os.system("pkill -o chromium")
                        os.system("killall chromium-browser")
                        src_renamPath = r'/var/www/html/indexcat9.php'
                        dst_renamPath = r'/var/www/html/index.php'
                        shutil.copy(src_renamPath, dst_renamPath)
                        os.system("chromium-browser localhost &")
                        time.sleep(0.2)
                        playpause = True
                #led9.off()
    '''upload and backup play functionality'''
    if but10.is_pressed:
        os.system("killall chromium-browser")
        print("buttons 10 pressed")
        previousTime = time.time()
        while but10.is_pressed:
            #Check if the button is pressed for > 2sec
            if time.time() - previousTime > 2.0:
                if but1.is_pressed or but2.is_pressed or but3.is_pressed \
                or but4.is_pressed or but5.is_pressed or but6.is_pressed \
                or but7.is_pressed or but8.is_pressed or but9.is_pressed:
                    # if button2 is also pressed and held, then shutdown the Pi
                    shutdownPi()
                # if the button is pressed for more than two seconds, then longpress is True
                longpress = True
                print("buttons 10 long pressed")
                time.sleep(0.5)
                print("button 10 short pressed")
                if nammaschoolradio:
                    os.system("pkill -9 aplay")
                    #Check whether the pendrive is connected
                    if rv1 == 0:
                        os.system("pkill -9 aplay")
                        print("Pendrive detected")
                        aplay("pendrivedetected.wav")
                        print("Pendrive name:",getDevName)
                        os.system("pkill -9 aplay")
                        aplay("copytouploadfolder.wav")
                        for x in range(1,10):
                            os.system("pkill -9 aplay")
                            #src path
                            pensrcpath = destpath1+str(x)
                            #dst path
                            updstpath = uploadpath1to9+str(x)
                            upfiles = os.listdir(pensrcpath)
                            if not upfiles:
                                os.system("pkill -9 aplay")
                                if x==1:
                                    print("No files to copy in cat",x)
                                    aplay("NothingToDownloadcat1.wav")
                                    continue
                                elif x==2:
                                    print("No files to copy in cat",x)
                                    aplay("NothingToDownloadcat2.wav")
                                    continue
                                elif x==3:
                                    print("No files to copy in cat",x)
                                    aplay("NothingToDownloadcat3.wav")
                                    continue
                                elif x==4:
                                    print("No files to copy in cat",x)
                                    aplay("NothingToDownloadcat4.wav")
                                    continue
                                elif x==5:
                                    print("No files to copy in cat",x)
                                    aplay("NothingToDownloadcat5.wav")
                                    continue
                                elif x==6:
                                    print("No files to copy in cat",x)
                                    aplay("NothingToDownloadcat6.wav")
                                    continue
                                elif x==7:
                                    print("No files to copy in cat",x)
                                    aplay("NothingToDownloadcat7.wav")
                                    continue
                                elif x==8:
                                    print("No files to copy in cat",x)
                                    aplay("NothingToDownloadcat8.wav")
                                    continue
                                elif x==9:
                                    print("No files to copy in cat",x)
                                    aplay("NothingToDownloadcat9.wav")
                                    continue
                            else:
                                for i in upfiles:
                                    os.system("pkill -9 aplay")
                                    if x==1:            
                                        print("copying to upload folder cat",x)
                                        aplay("Downloadcat1.wav")
                                    elif x==2:
                                        print("copying to upload folder cat",x)
                                        aplay("Downloadcat2.wav")
                                    elif x==3:
                                        print("copying to upload folder cat",x)
                                        aplay("Downloadcat3.wav")
                                    elif x==4:
                                        print("copying to upload folder cat",x)
                                        aplay("Downloadcat4.wav")
                                    elif x==5:
                                        print("copying to upload folder cat",x)
                                        aplay("Downloadcat5.wav")
                                    elif x==6:
                                        print("copying to upload folder cat",x)
                                        aplay("Downloadcat6.wav")
                                    elif x==7:
                                        print("copying to upload folder cat",x)
                                        aplay("Downloadcat7.wav")
                                    elif x==8:
                                        print("copying to upload folder cat",x)
                                        aplay("Downloadcat8.wav")
                                    elif x==9:
                                        print("copying to upload folder cat",x)
                                        aplay("Downloadcat9.wav")
                                    #print(localpath)
                                    #print(filename)
                                    src = pensrcpath+"/"+i
                                    dst = updstpath+"/"+i
                                    print(src)
                                    print(dst)
                                    shutil.copy(src, dst)
                                    print("Copied to upload folder cat",x)
                                aplay("Downloaded.wav")
                    elif playpause == True:
                        playpause = False
                        print ("echo closing radio !!!")
                        os.system("killall chromium-browser")
                        os.system("pkill -9 aplay")
                        time.sleep(0.2)
                        aplay("radiostop.wav")
                        break
                    #Check whether the local server is connected    
                    elif is_onradio() and is_connected(local_server):
                        print ("starting namma school radio....from local server ")
                        aplay("radiostart.wav")
                        time.sleep(0.4)
                        os.system("chromium-browser --app=http://"+local_server+" &")
                        playpause = True
                    # Check whether the internet is available to play from the website
                    elif is_connected(remote_server):
                        print ("starting namma school radio from internet")
                        os.system("pkill -9 aplay")
                        aplay("radiostart.wav")
                        time.sleep(0.4)
                        os.system("chromium-browser --app=https://www.namdu1radio.com/sadbhavana-radio &")                        
                        playpause = True
                    else:
                        print ("Button10 general play started")
                        os.system("pkill -9 aplay")
                        aplay("radiostart.wav")
                        src_renamPath = r'/var/www/html/index_original.php'
                        dst_renamPath = r'/var/www/html/index.php'
                        shutil.copy(src_renamPath, dst_renamPath)
                        #Starts playing mp3 from .upload folder
                        os.system("chromium-browser localhost &")
                        time.sleep(0.2)
                        playpause = True     
    
    
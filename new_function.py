import time
import os,sys
import socket
import subprocess
import wave
import contextlib
from datetime import datetime
from subprocess import check_output
import shutil
import logging
from globle_var import *




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
    os.system("arecord "+path+"/"+filename+" -D sysdefault:CARD=1 -f dat &")
    
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


def copy2Gdir_to_drvie(path1,path2,filename,recording_path):
    #Upload the file to respective category in google drive
    src_Path = 'rclone move'+" "+path1+"/"+filename+" "+path2+"/" 
    #dst_Path = destpath+"i"
    print(src_Path)
    #print(dst_Path)
    os.system(src_Path)
    print ("upload success !!!")
    time.sleep(0.1)


def record(button,stopaudio,recording_path,uploadpath,led=None):
            if led:
                led.on()
            print("recording has started")
            os.system("kill ll chromium-browser")
            os.system("pkill -o chromium")
            #time.sleep(0.4)
            #os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
            #aplay("beep_cat1.wav")
            time.sleep(1.0)
            # records with 48000 quality
            arecord(previewaudioguidepath,"recorded_audio.wav") 
            # scan for button press to stop recording
           
            button.wait_for_press(timeout=10) # to be discussed
            os.system("pkill -9 arecord")
            os.system("pkill -9 aplay")
            time.sleep(0.4)
            aplay(stopaudio)
            print("recording stopped")
            time.sleep(5.0)
            previewplay(previewaudioguidepath,"recorded_audio.wav")
            recFileName = "recorded@"+datetime.now().strftime('%d%b%Y_%H_%M_%S')
            # converting recorded audio to mp3 and rename with date and time of recording
            os.system("lame -b 320 "+previewaudioguidepath+"/recorded_audio.wav " +recording_path+"/"+recFileName+".mp3")
            #save the recorded audio in .upload folder respective category
            os.system("sudo cp "+recording_path+"/"+recFileName+".mp3 " +uploadpath+"/"+recFileName+".mp3 &")
            os.system("pkill -9 aplay")            
            #os.system("rm "+recording_path+"/recorded_audio.wav") #remove the recorded file 
    
def stop_radio(audio):    
    os.system("killall chromium-browser")
    os.system("pkill -o chromium")
    os.system("pkill -9 aplay")
    logging.info("closing the radio button")
    
    time.sleep(0.4)
    aplay(audio)       


def start_radio_from_internet():
    os.system("killall chromium-browser")
    os.system("pkill -o chromium")
    print ("starting namma school radio from internet")
    os.system("pkill -9 aplay")
    time.sleep(0.4)
    aplay("radiostart.wav")
    time.sleep(3.0)
    os.system("chromium-browser --kiosk --app=https://www.namdu1radio.com/thanmayi-school-radio &")     
#use first letter as a capital latter while defining catname
def playaudio(catname,led=None,preview_status=None):
            if led:                 
                led.on()
            global cat1playpause
            global playpause
            pfiles = os.listdir(uploadpathcat1)
            if preview_status == True:
                preview_status = False
                print(catname+" preview stopped")
                os.system("pkill -9 aplay")
                
            elif cat1playpause == True:
                stop_radio(stop_audio.radiostop)

                cat1playpause = False
                playpause = False
            elif is_connected(remote_server):
                start_radio_from_internet()
                   
                playpause = True
                cat1playpause = True
            elif not pfiles:
                print("No files to play in "+catname)
             #   aplay("NofilesinCat1.wav") ask girish ji about these files.
            else:
                os.system("pkill -9 aplay")
                time.sleep(0.4)
                aplay(audioguidepath,catname+".wav")
                time.sleep(0.4)
                os.system("killall chromium-browser")
                os.system("pkill -o chromium")
                src_renamPath = "/".join(uploadpath.split("/")[1:4])+'/indexcat1.php'
                dst_renamPath = "/".join(uploadpath.split("/")[1:4])+'/index.php'
                shutil.copy(src_renamPath, dst_renamPath)
                os.system("chromium-browser localhost &")
                time.sleep(0.2)
                playpause = True
                if led:               
                    led.off()
#!/usr/bin/python
# @brief: Script to upload files to google drive automatically
#         This script will be invoked on every boot
#
# @ver: 1.0
#---------------------------------------------------------------#
# **   * **** **   ** ***  *  *  **  ****  **** ***  ***** **** #
# * *  * *  * * * * * *  * *  * * *  *   * *  * *  *   *   *  * #
# *  * * **** *  *  * *  * *  *   *  ****  **** *  *   *   *  * #
# *   ** *  * *     * ***  ****  *** *    **  * ***  ***** **** #
#---------------------------------------------------------------#
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


# setting folder paths
projectpath =  os.path.split(os.path.realpath(__file__))[0]
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

		
''' 
	To check if wifi is local network
'''        
def is_onradio():
    try:
        test = "Namdu1Radio" in check_output("iwgetid", universal_newlines=True)
        return test
    except:
        return False

'''
    Function to get the name of the pendrive connected
'''    
def getDevName():
    '''The below code to identify the pendrive folder name - Start'''
    devlst = "ls /media/pi > /home/pi/Documents/python_script/usbs.txt"
    file1 = open('usbs.txt', 'r')
    Lines = file1.readlines()
    # Strips the newline character
    for line in Lines:
        line = line.rstrip("\n")
        if (line == '7022-5CC71'):
            penDet = False
            #print(line)
            #break;
        elif (line == '7022-5CC72'):
            penDet = False
            #print(line)
            #break;
        elif (line == '7022-5CC7'):
            penDet = False
            #print(line)
        else:
            var = line
            penDet = True
            print("Pendrive name:",var)
    return var
	
#destination path - Do not change the path
destpath_gdrive = "/home/pi/mnt/gdrive/cat" 
# network verification variables
remote_server = "www.google.com"
local_server = "192.168.1.50"
time.sleep(5)

while 1:
    #pendrive name
    devname =  getDevName()
    if penDet == True: 
        #update the destination path  
        destpath_pdrive = r"/media/pi/"+devname+r"/cat"	
        rv1 = subprocess.call("grep -qs '/media/pi' /proc/mounts", shell=True)
        rv2 = subprocess.call("mount | grep /media/pi", shell=True)
	# Get list of files in a directory
    for x in range(1, 10):
        #src path
        localpaths = recordingpath1to9+str(x)
        #dst path
        destpath = destpath_gdrive+str(x)
		destpath_pend = destpath_pdrive+str(x)
        print(localpaths)
        print("for loop x=%d",x)
        upfiles = os.listdir(localpaths)
        if not upfiles:
            #os.system("pkill -9 aplay")
            if x==1:
                print("No files to upload in cat",x)
                #aplay("NothingToUploadcat1.wav")
                continue
            elif x==2:
                print("No files to upload in cat",x)
                #aplay("NothingToUploadcat2.wav")
                continue
            elif x==3:
                print("No files to upload in cat",x)
                #aplay("NothingToUploadcat3.wav")
                continue
            elif x==4:
                print("No files to upload in cat",x)
                #aplay("NothingToUploadcat4.wav")
                continue
            elif x==5:
                print("No files to upload in cat",x)
                #aplay("NothingToUploadcat5.wav")
                continue
            elif x==6:
                print("No files to upload in cat",x)
                #aplay("NothingToUploadcat6.wav")
                continue
            elif x==7:
                print("No files to upload in cat",x)
                #aplay("NothingToUploadcat7.wav")
                continue
            elif x==8:
                print("No files to upload in cat",x)
                #aplay("NothingToUploadcat8.wav")
                continue
            elif x==9:
                print("No files to upload in cat",x)
                #aplay("NothingToUploadcat9.wav")
                continue
        else:
            if is_onradio() and is_connected(local_server):
                #os.system("pkill -9 aplay")
                print ("uploading to local server")
                aplay("sUploadinglocalserver.wav")
                for i in upfiles:
                    #os.system("pkill -9 aplay")
                    if x==1:
                        print("uploading to studio cat",x)
                        #aplay("sUploadingcat1.wav")
                    elif x==2:
                        print("uploading to studio cat",x)
                        #aplay("sUploadingcat2.wav")
                    elif x==3:
                        print("uploading to studio cat",x)
                        #aplay("sUploadingcat3.wav")
                    elif x==4:
                        print("uploading to studio cat",x)
                        #aplay("sUploadingcat4.wav")
                    elif x==5:
                        print("uploading to studio cat",x)
                        #aplay("sUploadingcat5.wav")
                    elif x==6:
                        print("uploading to studio cat",x)
                        #aplay("sUploadingcat6.wav")
                    elif x==7:
                        print("uploading to studio cat",x)
                        #aplay("sUploadingcat7.wav")
                    elif x==8:
                        print("uploading to studio cat",x)
                        #aplay("sUploadingcat8.wav")
                    elif x==9:
                        print("uploading to studio cat",x)
                        #aplay("sUploadingcat9.wav")   
                    os.system("sshpass -p 'raspberry' rsync "+localpaths+"/"+i+" pi@"+local_server+":/home/pi/Documents/pock1/")
                    os.system("rm "+localpaths+"/"+i)
                print ("upload success !!!")
                #aplay("Uploaded.wav")
            elif is_connected(remote_server):
                #os.system("pkill -9 aplay")
                #aplay("sUploadinginternet.wav")
                for i in upfiles:
                #os.system("pkill -9 aplay")
                if x==1:
                    print("uploading to internet cat",x)
                    #aplay("sUploadingcat1.wav")
                elif x==2:
                    print("uploading to internet cat",x)
                    #aplay("sUploadingcat2.wav")
                elif x==3:
                    print("uploading to internet cat",x)
                    #aplay("sUploadingcat3.wav")
                elif x==4:
                    print("uploading to internet cat",x)
                    #aplay("sUploadingcat4.wav")
                elif x==5:
                    print("uploading to internet cat",x)
                    #aplay("sUploadingcat5.wav")
                elif x==6:
                    print("uploading to internet cat",x)
                    #aplay("sUploadingcat6.wav")
                elif x==7:
                    print("uploading to internet cat",x)
                    #aplay("sUploadingcat7.wav")
                elif x==8:
                    print("uploading to internet cat",x)
                    #aplay("sUploadingcat8.wav")
                elif x==9:
                    print("uploading to internet cat",x)
                    #aplay("sUploadingcat9.wav")
                #Upload the file to respective category in google drive
                src_Path = 'rclone move'+" "+localpaths+"/"+i+" "+destpath+"/" 
                #dst_Path = destpath+"i"
                print(src_Path)
                #print(dst_Path)
                os.system(src_Path)
                print ("upload success !!!")
                #os.system("pkill -9 aplay")
                #aplay("Uploaded.wav")				
            elif rv1 == 0:
                print("Pendrive detected")
                #aplay("pendrivedetected.wav")
                print("Pendrive name:",getDevName) 
                #aplay("copytopendrive.wav")
                for i in upfiles:
                    print("copying files to pendrive")
                    src = localpaths+"/"+i
                    dst = destpath_pend+"/"+i
                    print(src)
                    print(dst)
                    shutil.copy(src, dst)                        
                    print ("Files copied to pendrive successfully !!!")                                
            else:
                #os.system("pkill -9 aplay")
                print("No internet!!! connection to upload to Gdrive!")
                #aplay("Nointernet.wav")        
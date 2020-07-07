#!/usr/bin/python
# @brief: Script to upload files to google drive automatically
#         This script will be invoked on every boot
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

''' *** Global variables *** '''
penDet = False
#destination path - Do not change the path
destpath_gdrive = "/home/pi/mnt/gdrive/cat"

gdrivepath_broadcast = "/home/pi/mnt/gdrive/Ready_To_Broadcast/cat"
# network verification variables
remote_server = "www.google.com"
local_server = "192.168.1.50"

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
    Macro for playing audio instructions - to keep the code simple
'''
def aplay(filename):
    os.system("aplay -D plughw:CARD=0,DEV=0 "+audioguidepath+"/"+filename)

'''
    Function to get the name of the pendrive connected
'''    
def getDevName():
    '''The below code to identify the pendrive folder name - Start'''
    os.system('rm -rf /home/pi/Documents/Namdu1Radio/usbs/usbs.txt')
    os.system('ls /media/pi > /home/pi/Documents/Namdu1Radio/usbs/usbs.txt')
    file1 = open("/home/pi/Documents/Namdu1Radio/usbs/usbs.txt", "r")
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


while True:
    ''' The following code for Uploading files to localserver or Gdrive or pendrive '''
    #pendrive name
    devname =  getDevName()
    if penDet == True:
        #update the destination path  
        destpath_pdrive = r"/media/pi/"+devname+r"/cat" 
        rv1 = subprocess.call("grep -qs '/media/pi' /proc/mounts", shell=True)
        rv2 = subprocess.call("mount | grep /media/pi", shell=True)
        penDet = False
    # Get list of files in a directory
    for x in range(1, 10):
        #src path
        localpaths = recordingpath1to9+str(x)
        #dst path
        destpath = destpath_gdrive+str(x)
        if penDet == True:
            destpath_pend = destpath_pdrive+str(x)
        print(localpaths)
        #print("for loop x=%d",x)
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
                #aplay("sUploadinglocalserver.wav")
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
                    os.system("pkill -9 aplay")
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
                    time.sleep(0.1)
            elif rv1 == 0:
                print("Pendrive detected")
                #aplay("pendrivedetected.wav")
                print("Pendrive name:",getDevName) 
                #aplay("copytopendrive.wav")
                for i in upfiles:
                    print("copying files to pendrive")
                    src0 = localpaths+"/"+i
                    dst0 = destpath_pend+"/"+i
                    print(src0)
                    print(dst0)
                    shutil.copy(src0, dst0)                        
                    print ("Files copied to pendrive successfully !!!")                                
            else:
                print("No internet!!! connection to upload to Gdrive!")
                #aplay("Nointernet.wav")
    ''' The following code for downloading files from Gdrive, pendrive to .upload folder '''                
    # Get list of files in a directory
    if is_connected(remote_server):
        for y in range(1, 10):
            #src path
            gdrivepath = gdrivepath_broadcast+str(y)
            #dst path
            destpath_up = uploadpath+str(y)
            #print("for loop x=%d",y)
            dwnfiles = os.listdir(gdrivepath)
            if not dwnfiles:
                #os.system("pkill -9 aplay")
                if y==1:
                    print("No files to Download in cat",y)
                    #aplay("NothingToUploadcat1.wav")
                    continue
                elif y==2:
                    print("No files to Download in cat",y)
                    #aplay("NothingToUploadcat2.wav")
                    continue
                elif y==3:
                    print("No files to Download in cat",y)
                    #aplay("NothingToUploadcat3.wav")
                    continue
                elif y==4:
                    print("No files to Download in cat",y)
                    #aplay("NothingToUploadcat4.wav")
                    continue
                elif y==5:
                    print("No files to Download in cat",y)
                    #aplay("NothingToUploadcat5.wav")
                    continue
                elif y==6:
                    print("No files to Download in cat",y)
                    #aplay("NothingToUploadcat6.wav")
                    continue
                elif y==7:
                    print("No files to Download in cat",y)
                    #aplay("NothingToUploadcat7.wav")
                    continue
                elif y==8:
                    print("No files to Download in cat",y)
                    #aplay("NothingToUploadcat8.wav")
                    continue
                elif y==9:
                    print("No files to Download in cat",y)
                    #aplay("NothingToUploadcat9.wav")
                    continue
            else:
                for j in dwnfiles:
                    print("copying files to upload folder")
                    src1 = gdrivepath+"/"+j
                    dst1 = destpath_up+"/"+j
                    print(src1)
                    print(dst1)
                    shutil.copy(src1, dst1)                        
                    print ("Files copied to upload folder successfully !!!")
    else:
        if rv1 == 0:
            print("Pendrive detected")
            #aplay("pendrivedetected.wav")
            print("Pendrive name:",getDevName)
            #os.system("pkill -9 aplay")
            #aplay("copytouploadfolder.wav")
            for y in range(1,10):
                #os.system("pkill -9 aplay")
                #src path
                pensrcpath = destpath_pdrive+str(y)
                #dst path
                updstpath = uploadpath1to9+str(y)
                upfiles = os.listdir(pensrcpath)
                if not upfiles:
                    #os.system("pkill -9 aplay")
                    if y==1:
                        print("No files to copy in cat",y)
                        #aplay("NothingToDownloadcat1.wav")
                        continue
                    elif y==2:
                        print("No files to copy in cat",y)
                        #aplay("NothingToDownloadcat2.wav")
                        continue
                    elif y==3:
                        print("No files to copy in cat",y)
                        #aplay("NothingToDownloadcat3.wav")
                        continue
                    elif y==4:
                        print("No files to copy in cat",y)
                        #aplay("NothingToDownloadcat4.wav")
                        continue
                    elif y==5:
                        print("No files to copy in cat",y)
                        #aplay("NothingToDownloadcat5.wav")
                        continue
                    elif y==6:
                        print("No files to copy in cat",y)
                        #aplay("NothingToDownloadcat6.wav")
                        continue
                    elif y==7:
                        print("No files to copy in cat",y)
                        #aplay("NothingToDownloadcat7.wav")
                        continue
                    elif y==8:
                        print("No files to copy in cat",y)
                        #aplay("NothingToDownloadcat8.wav")
                        continue
                    elif y==9:
                        print("No files to copy in cat",y)
                        #aplay("NothingToDownloadcat9.wav")
                        continue
                else:
                    for j in dwnfiles:
                        #os.system("pkill -9 aplay")
                        if y==1:            
                            print("copying to upload folder cat",y)
                            #aplay("Downloadcat1.wav")
                        elif y==2:
                            print("copying to upload folder cat",y)
                            #aplay("Downloadcat2.wav")
                        elif y==3:
                            print("copying to upload folder cat",y)
                            #aplay("Downloadcat3.wav")
                        elif y==4:
                            print("copying to upload folder cat",y)
                            #aplay("Downloadcat4.wav")
                        elif y==5:
                            print("copying to upload folder cat",y)
                            #aplay("Downloadcat5.wav")
                        elif y==6:
                            print("copying to upload folder cat",y)
                            #aplay("Downloadcat6.wav")
                        elif y==7:
                            print("copying to upload folder cat",y)
                            #aplay("Downloadcat7.wav")
                        elif y==8:
                            print("copying to upload folder cat",y)
                            #aplay("Downloadcat8.wav")
                        elif y==9:
                            print("copying to upload folder cat",y)
                            #aplay("Downloadcat9.wav")
                        #print(localpath)
                        #print(filename)
                        src = pensrcpath+"/"+j
                        dst = updstpath+"/"+j
                        print(src)
                        print(dst)
                        shutil.copy(src, dst)
                        print("Copied to upload folder cat",y)        
        
                
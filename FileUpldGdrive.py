#!/usr/bin/python
# @brief: Script to upload files to google drive and download files
#         automatically .upload folder.
#         This script will be invoked on boot.
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
recordingpathcat10 = projectpath + "/recordings/cat10"
recordingpathgencat = projectpath + "/recordings/gencat"

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
uploadpathgencat = uploadpath + "/gencat"

''' *** Global variables *** '''
penDet = False
ret = None
found = False
#destination path - Do not change the path
destpath_gdrive = "/home/pi/mnt/gdrive/cat"
destpath_gdrivegencat = "/home/pi/mnt/gdrive/gencat"
gdrivepath_broadcast = "/home/pi/mnt/gdrive/Ready_To_Broadcast/cat"
gdrivepath_broadcastgencat = "/home/pi/mnt/gdrive/Ready_To_Broadcast/gencat"
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
        ret = line
        penDet = True
        print("Pendrive name:",ret)
        return ret
 
 
'''
    copy files to gdrive
'''
def copy2Gdrive(path1,path2,filename):
    #Upload the file to respective category in google drive
    src_Path = 'rclone move'+" "+path1+"/"+filename+" "+path2+"/" 
    #dst_Path = destpath+"i"
    print(src_Path)
    #print(dst_Path)
    os.system(src_Path)
    print ("upload success !!!")
    time.sleep(0.1)    
 
os.system("sudo chmod -R 777 /var/www/html/.upload") 
time.sleep(16)
while True:
    ''' The following code for Uploading files to localserver or Gdrive or pendrive '''
    #pendrive name
    devname =  getDevName()
    if devname != None:
        #update the destination path  
        destpath_pdrive = r"/media/pi/"+devname+r"/cat"
        destpath_pdrivegencat = r"/media/pi/"+devname+r"/gencat"
        rv1 = subprocess.call("grep -qs '/media/pi' /proc/mounts", shell=True)
        rv2 = subprocess.call("mount | grep /media/pi", shell=True)
        penDet = False
    # Get list of files in a directory
    for x in range(1, 12):
        #src path
        localpaths = recordingpath1to9+str(x)
        #dst path
        destpath = destpath_gdrive+str(x)
        if devname != None:#if pendrive is connected
            destpath_pend = destpath_pdrive+str(x)
        print(localpaths)
        #print("for loop x=%d",x)
        if not x==11:
            upfiles = os.listdir(localpaths)
        if x==11:
            #src path
            localpaths = recordingpathgencat
            #dst path
            destpath = destpath_gdrivegencat
            if devname != None:#if pendrive is connected
                destpath_pend = destpath_pdrivegencat
            print(localpaths)
            #print("for loop x=%d",x)
            upfiles = os.listdir(localpaths)   
        if not upfiles:
            #os.system("pkill -9 aplay")
            if x == 1 or x == 2 or x == 3 or x == 4 \
            or x == 5 or x == 6 or x == 7 or x == 8 \
            or x == 9 or x == 10 or x == 11:
                print("No files to upload in cat",x)
                #aplay("NothingToUploadcat1.wav")
                continue
        else:
            if is_onradio() and is_connected(local_server):
                #os.system("pkill -9 aplay")
                print ("uploading to local server")
                #aplay("sUploadinglocalserver.wav")
                for i in upfiles:
                    #os.system("pkill -9 aplay")
                    if x == 1 or x == 2 or x == 3 or x == 4 \
                    or x == 5 or x == 6 or x == 7 or x == 8 \
                    or x == 9 or x == 10 or x == 11:
                        print("uploading to studio cat",x)
                        #aplay("sUploadingcat1.wav")
                    os.system("sshpass -p 'raspberry' rsync "+localpaths+"/"+i+" pi@"+local_server+":/home/pi/Documents/pock1/")
                    os.system("rm "+localpaths+"/"+i)
                print ("upload success !!!")
                #aplay("Uploaded.wav")
            elif is_connected(remote_server):
                #os.system("pkill -9 aplay")
                #aplay("sUploadinginternet.wav")
                for i in upfiles:
                    if x == 1 or x == 2 or x == 3 or x == 4 \
                    or x == 5 or x == 6 or x == 7 or x == 8 \
                    or x == 9 or x == 10 or x == 11:
                        chkfiles = os.listdir(destpath)
                        if not chkfiles:
                            print("uploading to internet cat",x)
                            #aplay("sUploadingcat1.wav")
                            copy2Gdrive(localpaths,destpath,i)
                        else:
                            for j in chkfiles:
                                if i == j:
                                    found = True
                                    print("File already exists:",i)
                                    os.system("rm "+localpaths+"/"+i)
                                    continue
                            if found == False:
                                print("uploading to internet cat",x)
                                #aplay("sUploadingcat1.wav")
                                copy2Gdrive(localpaths,destpath,i)
                                #found = False
                            else:
                                found = False
                    else:
                        print("Dummy print")    
            elif rv1 == 0:
                print("Pendrive detected")
                #aplay("pendrivedetected.wav")
                #print("Pendrive name:",getDevName)
                #aplay("copytopendrive.wav")
                for i in upfiles:
                    print("copying files to pendrive")
                    src0 = localpaths+"/"+i
                    dst0 = destpath_pend
                    chkfiles = os.listdir(dst0)
                    if not chkfiles:
                        print("uploading to pendrive cat",x)
                        shutil.copy(src0, dst0)
                        os.system("rm "+src0)
                    else:
                        for j in chkfiles:
                            if i == j:
                                found = True
                                print("File already exists in pendrive:",i)
                                os.system("rm "+src0)
                                continue
                        if found == False:
                            print("uploading to pendrive cat",x)
                            #aplay("sUploadingcat1.wav")
                            shutil.copy(src0, dst0)
                            os.system("rm "+src0)                                    
                            #found = False
                        else:
                            found = False
                    #print(src0)
                    #print(dst0)
                    #shutil.copy(src0, dst0)                        
                    print ("Files copied to pendrive successfully !!!")                                
            else:
                print("No internet!!! No Pendrive !!! No localserver available!!!")
                #aplay("Nointernet.wav")
    ''' The following code for downloading files from Gdrive/Pendrive to .upload folder '''                
    # Get list of files in a directory
    if is_connected(remote_server):
        for y in range(1, 12):
            #src path
            gdrivepath = gdrivepath_broadcast+str(y)
            #dst path
            destpath_up = uploadpath+str(y)
            if y==11:
                #src path
                gdrivepath = gdrivepath_broadcastgencat
                #dst path
                destpath_up = uploadpathgencat
            #print("for loop x=%d",y)
            dwnfiles = os.listdir(gdrivepath)
            if not dwnfiles:
                #os.system("pkill -9 aplay")
                if y == 1 or y == 2 or y == 3 or y == 4 \
                or y == 5 or y == 6 or y == 7 or y == 8 \
                or y == 9 or y == 10 or y == 11:
                    print("No files to Download in cat",y)
                    #aplay("NothingToUploadcat1.wav")
                    continue                
            else:
                for k in dwnfiles:
                    if y == 1 or y == 2 or y == 3 or y == 4 \
                    or y == 5 or y == 6 or y == 7 or y == 8 \
                    or y == 9 or y == 10 or y == 11:            
                        print("copying to upload folder cat",y)                    
                        src1 = gdrivepath+"/"+k
                        dst1 = destpath_up+"/"+k
                        chkfiles = os.listdir(destpath_up)
                        if not chkfiles:
                            print("downloading to .upload cat",y)
                            shutil.copy(src1, dst1)
                            os.system("rm "+src1)
                        else:
                            for l in chkfiles:
                                if k == l:
                                    found = True
                                    print("File already exists in pendrive:",k)
                                    os.system("rm "+src1)
                                    continue
                            if found == False:
                                print("uploading to pendrive cat",y)
                                #aplay("sUploadingcat1.wav")
                                shutil.copy(src1, dst1)
                                os.system("rm "+src1)
                                #found = False
                            else:
                                found = False
                    #print(src1)
                    #print(dst1)
                    #shutil.copy(src1, dst1)                        
                    print ("Files copied to upload folder successfully !!!")
    else:
        if devname != None:
            print("Pendrive detected")
            #aplay("pendrivedetected.wav")
            print("Pendrive name:",getDevName)
            #os.system("pkill -9 aplay")
            #aplay("copytouploadfolder.wav")
            for y in range(1,12):
                #os.system("pkill -9 aplay")
                #src path
                pensrcpath = destpath_pdrive+str(y)
                #dst path
                updstpath = uploadpath1to9+str(y)
                if y==11:
                    #src path
                    pensrcpath = destpath_pdrivegencat
                    #dst path
                    updstpath = uploadpathgencat
                dwnfiles = os.listdir(pensrcpath)
                if not dwnfiles:
                    #os.system("pkill -9 aplay")
                    if y == 1 or y == 2 or y == 3 or y == 4 \
                    or y == 5 or y == 6 or y == 7 or y == 8 \
                    or y == 9 or y == 10 or y == 11:
                        print("No files to copy from pendrive to .upload cat",y)
                        #aplay("NothingToDownloadcat1.wav")
                        continue              
                else:
                    for k in dwnfiles:
                        #os.system("pkill -9 aplay")
                        if y == 1 or y == 2 or y == 3 or y == 4 \
                        or y == 5 or y == 6 or y == 7 or y == 8 \
                        or y == 9 or y == 10 or y == 11:            
                            print("copying to upload folder cat",y)                    
                            src1 = pensrcpath+"/"+k
                            dst1 = updstpath+"/"+k
                            chkfiles = os.listdir(updstpath)
                            if not chkfiles:
                                print("downloading to .upload cat",y)
                                shutil.copy(src1, dst1)
                                os.system("rm "+src1)
                            else:
                                for l in chkfiles:
                                    if k == l:
                                        found = True
                                        print("File already exists in pendrive:",k)
                                        os.system("rm "+src1)
                                        continue
                                if found == False:
                                    print("uploading to pendrive cat",y)
                                    #aplay("sUploadingcat1.wav")
                                    shutil.copy(src1, dst1)
                                    os.system("rm "+src1)                                    
                                    #found = False
                                else:
                                    found = False
                            #aplay("Downloadcat1.wav")

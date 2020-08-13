import os
from datetime import datetime
import wave

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


cntr = True
recFileName = "record"

recFileName = "recorded@"+datetime.now().strftime('%d%b%Y_%H_%M_%S')
print(recFileName)



# converting recorded audio to mp3 and rename with date and time of recording
os.system("lame -b 320 "+previewaudioguidepath+"/recorded_audio.wav " +recordingpathcat1+"/"+recFileName+".mp3")
os.system("sudo cp "+recordingpathcat1+"/"+recFileName+".mp3 " +uploadpathcat1+"/"+recFileName+".mp3 &")
#os.system("cp "+recordingpathcat10+"/recorded_audio.wav" +localplaypath+"/recorded@"+datetime.now().strftime('%d%b%Y_%H:%M')+".wav &")
#os.system("sudo lame -b 320 "+previewaudioguidepath+"/recorded_audio.wav " +uploadpathcat11+"/recorded@"+datetime.now().strftime('%d%b%Y_%H:%M')+".mp3 &")



'''
if cntr == True:
    os.system('rm -rf /home/pi/Documents/Namdu1Radio/usbs.txt')
    os.system('ls /media/pi > /home/pi/Documents/Namdu1Radio/usbs.txt')
    print("operation done")
    cntr = False
else:
    print("operation done")
'''    
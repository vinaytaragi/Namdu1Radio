import os
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
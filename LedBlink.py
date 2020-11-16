import os
from time import sleep
from gpiozero import Button
from dualled import DualLED
import RPi.GPIO as GPIO

but11 = Button(26) #26 - cat11
led = None

led = DualLED(21,24)
GPIO.setmode(GPIO.BCM)
path = "/home/pi/Documents/Namdu1Radio/recordings"
filename = "testblinkrec.wav"

led.off()
led.fwd_blink("slow")
os.system("arecord "+path+"/"+filename+" -D sysdefault:CARD=2 -f dat &")
but11.wait_for_press()
os.system("pkill arecord")
led.off()
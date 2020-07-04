import os

cntr = True

if cntr == True:
    os.system('rm -rf /home/pi/Documents/Namdu1Radio/usbs.txt')
    os.system('ls /media/pi > /home/pi/Documents/Namdu1Radio/usbs.txt')
    print("operation done")
    cntr = False
else:
    print("operation done")
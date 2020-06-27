#  Welcome to Namdu1Radio 

# Basic settings before starting Pi
1. Clone the repository to this path "/home/pi/Documents/"

2. Open "autostart" form your favourite editor (file path: /home/pi/.config/lxsession/LXDE-pi)
   Delete the "@python /home/pi/Documents/python_script/lappi.py &" line and add the below lines
   @python /home/pi/Documents/Namdu1Radio/mountdrive.py &
   @python /home/pi/Documents/Namdu1Radio/FileUpld2Gdrive.py &
   @python /home/pi/Documents/Namdu1Radio/MultiCat_Radio.py &
   
# Python Files info 
  mountdrive.py -> Is used for mounting the google drive automatically on boot.
  
  FileUpld2Gdrive.py -> Is used to upload a file to localserver/google drive/pendrive on boot.
  
  MultiCat_Radio.py -> Is used to record,play the radio for different categories. Currently we are supoorting recording of 9 different categories. This pyhton file called   automatically on boot.
  
Please refer the "Namdu1radio_HSD.doc" for more detailed info..

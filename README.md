#  Welcome to Namdu1Radio 

# Basic settings before starting Pi
1. Open a terminal and enter this command "cd /home/pi/Documents/"

2. Clone the repository enter this command in terminal "git clone https://github.com/Pragathi-Foundation/Namdu1Radio.git"

2. Open "autostart" form your favourite editor (file path: /home/pi/.config/lxsession/LXDE-pi)
   Delete the "@python /home/pi/Documents/python_script/lappi.py &" line and add the below lines
   
   @python /home/pi/Documents/Namdu1Radio/radio.py &
   
   @python /home/pi/Documents/Namdu1Radio/FileUpld2Gdrive.py &
   
# Python Files info 
    
  FileUpld2Gdrive.py -> Is used to upload a file to localserver/google drive/pendrive on boot.
  
  radio.py -> Is used to mount gdrive, record and play the radio for different categories. Currently we are supoorting recording of 11 different categories. This pyhton file is invoked   automatically on boot.
  
Please refer the "Namdu1radio_HSD.doc" for more detailed info..

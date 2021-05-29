import os

def copy2Gdir_to_drvie(path1,path2,filename):
    #Upload the file to respective category in google drive
    src_Path = 'rclone move'+" "+path1+"/"+filename+" "+path2+"/" 
    #dst_Path = destpath+"i"
    print(src_Path)
    #print(dst_Path)
    os.system(src_Path)
    print ("upload success !!!")
    time.sleep(0.1)
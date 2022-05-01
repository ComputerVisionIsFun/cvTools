import cv2
import numpy as np
import os 

def video2frames(folder, list_path, save_folder, save_start_i=0, period = 120):
    save_i = save_start_i
    for path in list_path:
        cap = cv2.VideoCapture(folder + path)
        
        frame_i = 0
        while(1):
            ret, frame = cap.read()
            if ret==False:
                break

            if frame_i%period==1:
                save_path = save_folder + str(save_i) + '.png'
                cv2.imwrite(save_path, frame)
                save_i+=1

            frame_i+=1
            


# 
video2frames('C:/Users/Chiang-En Chen/Desktop/',['2-lan.avi'],'D:/Dataset/lpr_2/',0,5)


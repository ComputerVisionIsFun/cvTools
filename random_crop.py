import cv2
import random
import argparse
import os


CROP_WIDTH = 24
CROP_HEIGHT = 24
IMG_FOLDER = 'D:/Dataset/Face_detection/bg/'
NUM_CROP = 125855
CROP_SAVE_FOLDER = 'D:/Dataset/Face_detection/crop_bg/'


filenames = os.listdir(IMG_FOLDER)
crop_save_i = 0
while(crop_save_i<NUM_CROP):

    ind = random.randint(0, len(filenames) - 1)
    resize = random.randint(50, 300)/100
    try:
        file_path = IMG_FOLDER + filenames[ind]
        img = cv2.imread(file_path, 0)
        width, height = img.shape[1], img.shape[0]
        img = cv2.resize(img, (int(width/resize), int(height/resize)), 1)
        x, y = random.randint(0, img.shape[1] - CROP_WIDTH - 1), random.randint(0, img.shape[0] - CROP_HEIGHT - 1)
        crop = img[y:y+CROP_HEIGHT, x:x + CROP_WIDTH]
        cv2.imwrite(CROP_SAVE_FOLDER + str(crop_save_i) + '.png', crop)
        crop_save_i+=1
    except:
        continue













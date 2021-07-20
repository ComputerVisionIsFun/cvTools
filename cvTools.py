import cv2
import numpy as np
import os
'''
cv bgr img is of shape h x w x c
'''

def _random_crop(bgr, crop_w=24, crop_h=24):
    random_x = np.random.randint(0, bgr.shape[1] - crop_w)
    random_y = np.random.randint(0, bgr.shape[0] - crop_h)
    return bgr[random_y:random_y+crop_h, random_x:random_x+crop_w, :].copy()

def _random_brightness(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    return 

def _padding(bgr, pw=1, ph=1):
    return 




def random_crop(img_folder='/', save_folder='/', save_header='1_',crop_w = 24, crop_h = 24, num_crop = 10):
    img_names = os.listdir(img_folder)
    clean_img_names = []
    try:
        os.mkdir(save_folder)
    except:
        1

    for img_name in img_names:
        print(img_name[-3:])
        if img_name[-3:] in ['png', 'bmp', 'jpg','peg']:
            clean_img_names.append(img_name)

    for crop_i in range(num_crop):
        id = np.random.randint(0, len(clean_img_names))
        img = cv2.imread(img_folder + clean_img_names[id], 1)
        img_crop = _random_crop(img, crop_w=crop_w, crop_h=crop_h)
        save_path = save_folder + save_header + str(crop_i) + '.png'
        cv2.imwrite(save_path, img_crop)




        
        
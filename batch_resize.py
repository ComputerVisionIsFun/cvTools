import cv2
import os

RESIZE_WIDTH = 24
RESIZE_HEIGHT = 24
SAVE_FOLDER = 'D:/Dataset/face/img_align_celeba/24_faces/'
# IMG_FOLDER = 'D:/Dataset/face/img_align_celeba/crop_img_align_celeba/'
IMG_FOLDER = 'D:/Dataset/face_mix/'
FLIP = True
filenames = os.listdir(IMG_FOLDER)
save_i = 0
for filename in filenames:
    try:
        if filename[-1]=='p' or filename[-1]=='g':
            img_path = IMG_FOLDER + filename
            img = cv2.imread(img_path, 0)
            img = cv2.resize(img, (RESIZE_WIDTH,RESIZE_HEIGHT),1)

            if FLIP:
                cv2.imwrite(SAVE_FOLDER + str(save_i) + '.png', img)
                save_i+=1
                img = cv2.flip(img, 1)
                cv2.imwrite(SAVE_FOLDER + str(save_i) + '.png', img)
                save_i+=1 
            else:
                cv2.imwrite(SAVE_FOLDER + str(save_i) + '.png', img)
                save_i += 1

    except:
        continue


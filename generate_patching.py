import cv2
import os
import random

NUM_OBJS = 30
BG_PATH = 'D:/Dataset/faces_bg/bg/2.png'
OBJ_IMG_FOLDER = 'D:/Dataset/face/img_align_celeba/24_faces/'
SAVE_PATH = 'D:/GitHub/light-face-detector/test_imgs/test1.png'

bg = cv2.imread(BG_PATH, 0)
face_filenames = os.listdir(OBJ_IMG_FOLDER)

for face_i in range(NUM_OBJS):
    ind = random.randint(0, len(face_filenames) - 1)
    face_filename = face_filenames[ind]
    try:
        face = cv2.imread(OBJ_IMG_FOLDER + face_filename, 0)
        x = random.randint(0, bg.shape[1] - face.shape[1] - 10)
        y = random.randint(0, bg.shape[0] - face.shape[0] - 10)
        bg[y:y+face.shape[0], x:x+face.shape[1]] = face

    except:
        continue
    
cv2.imwrite(SAVE_PATH, bg)

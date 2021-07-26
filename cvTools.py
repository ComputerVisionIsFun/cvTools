import cv2
import numpy as np
import os
'''
cv bgr img is of shape h x w x c
'''

def _random_crop(bgr, crop_w=24, crop_h=24):
    if (bgr.shape[0]<=crop_w + 5) or (bgr.shape[0]<=crop_h + 5):
        bgr = cv2.resize(bgr, (crop_w + 5, crop_h + 5))

    random_x = np.random.randint(0, bgr.shape[1] - crop_w)
    random_y = np.random.randint(0, bgr.shape[0] - crop_h)
    return bgr[random_y:random_y+crop_h, random_x:random_x+crop_w, :].copy()

def _random_brightness(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    ratio = np.random.randint(10, 50)/20
    if hsv[:, :, 2].mean()/ratio<=37:
        return bgr
    else:
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


def _random_resize(bgr):
    r = np.random.randint(2, 5)
    # print('resize', bgr.shape)
    output = cv2.resize(bgr, (int(bgr.shape[1]/r), int(bgr.shape[1]/r)))
    
    return output

def random_crop(img_folder='/', save_folder='/', save_header='1_',crop_w = 24, crop_h = 24, num_crop = 10):
    img_names = os.listdir(img_folder)
    clean_img_names = []
    try:
        os.mkdir(save_folder)
    except:
        1

    for img_name in img_names:
        
        if img_name[-3:] in ['png', 'bmp', 'jpg','peg']:
            clean_img_names.append(img_name)

    for crop_i in range(num_crop):
        id = np.random.randint(0, len(clean_img_names))
        # print(clean_img_names[id])
        img = cv2.imread(img_folder + clean_img_names[id], 1)
        # print('resize', img.shape)
        if np.random.randint(1, 3)%2==0:
            img = _random_brightness(img)
        if np.random.randint(1, 3)%2==0:
            img = _random_resize(img)
        img_crop = _random_crop(img, crop_w=crop_w, crop_h=crop_h)
        save_path = save_folder + save_header + str(crop_i) + '.png'
        cv2.imwrite(save_path, img_crop)


def patching(bgr, crop):
    w, h = crop.shape[1], crop.shape[0]
    x = np.random.randint(0, bgr.shape[1] - crop.shape[1])
    y = np.random.randint(0, bgr.shape[0] - crop.shape[0])
    bgr[y:y+h, x:x+w, :] = crop
    return bgr

        
def extract_frames_from_videos(video_path, save_folder = '/', save_title = '1_', period = 10):
    cap = cv2.VideoCapture(video_path)
    # 
    if (cap.isOpened()==False):
        print("Error opening video stream of file.")

    # 
    save_i = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            if save_i%period==0:
                cv2.imwrite(save_folder + save_title + str(save_i) + '.png', frame)

            # if cv2.waitKey(25)&0xFF==ord('q'):
                # break
            save_i+=1
        else:
            break

    cap.release()
    # cv2.destroyAllWindows()
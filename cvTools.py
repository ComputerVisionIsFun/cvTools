import cv2
import numpy as np
import os
import xml.etree.ElementTree as ET
import pandas as pd
import random
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



# xml 
def create_an_object(name:str, xmin:str, ymin:str, xmax:str, ymax:str):
    obj_elements = ['name','pose','truncated','difficult','bndbox']
    new_element = ET.Element('object')
    
    # 
    for obj_element in obj_elements:
        ET.SubElement(new_element, obj_element)
        ET.dump(new_element)

    new_element[0].text = name
    new_element[1].text = 'Unspeicfied'
    new_element[2].text = '0'
    new_element[3].text = '0'
    
    # check 
    # print(float(xmin), float(xmax), float(ymin), float(ymax))
    if float(xmin)>=float(xmax) or float(ymin)>=float(ymax): 
        print('ValueError:xmin>=xmax or ymin>=ymax')
        return 

    # edit bndbox
    bndbox_elements = ['xmin','ymin','xmax','ymax']
    for i, ele in enumerate(bndbox_elements):
        ET.SubElement(new_element[4], ele)
        ET.dump(new_element[4])

        if ele=='xmin':
            new_element[4][i].text = xmin
        elif ele=='ymin':
            new_element[4][i].text = ymin
        elif ele=='xmax':
            new_element[4][i].text = xmax
        else:
            new_element[4][i].text = ymax

    return new_element

def patching_xml(labeling_main_folder, labeling_sub_folder, bg_folder, bg_name,obj_label, obj_folder, num_objs,save_title, sample_xml_path = 'sample.xml'):
    obj_names = os.listdir(obj_folder)
    bg_img = cv2.imread(bg_folder + bg_name, 1)
    bg_ref = np.zeros(bg_img.shape, dtype='uint8')
    save_img_format = '.jpg'
    # read the sample xml
    tree = ET.parse(sample_xml_path)
    root = tree.getroot()

    root.find('folder').text = labeling_sub_folder.replace('/','')
    root.find('filename').text = save_title + save_img_format
    root.find('path').text = labeling_main_folder + labeling_sub_folder + save_title + '.' + save_img_format
    root.find('size').find('width').text = str(bg_img.shape[1])
    root.find('size').find('height').text = str(bg_img.shape[0])
    root.find('size').find('depth').text = '3'

    output = bg_img.copy()

    # 
    # random.shuffle(obj_names)
    
    for obj_i in range(num_objs):
        obj_ind = random.randint(0, len(obj_names) - 1)
        obj_path = obj_folder + obj_names[obj_ind]
        obj = cv2.imread(obj_path, 1)

        #ai. add img
        bg_now = np.zeros(bg_img.shape,dtype='uint8')
        indicator = np.ones(obj.shape, dtype='uint8')
        width, height = indicator.shape[1], indicator.shape[0]
        random_x = random.randint(0, bg_now.shape[1] - width - 2)
        random_y = random.randint(0, bg_now.shape[0] - height - 2)

        bg_now[random_y:random_y + height, random_x:random_x + width, :] = indicator

        if (bg_now*bg_ref).sum()>0:
            continue
        else:
            # step 1. patching
            output[random_y:random_y+height, random_x:random_x+width, :] = obj

            # step 2. update bg_ref
            bg_ref[random_y:random_y + height, random_x:random_x + width, :] = indicator
            
            # step 3. add an object into xml
            xmin, ymin = str(random_x), str(random_y)
            xmax, ymax = str(random_x + width - 1), str(random_y + height - 1) 
            new_element = create_an_object(obj_label, xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)
            root.insert(6, new_element)

        

    # save img and xml
    img_save_path = labeling_main_folder + labeling_sub_folder + save_title + save_img_format
    cv2.imwrite(img_save_path, output)
    xml_save_path = labeling_main_folder + labeling_sub_folder + save_title + '.xml'
    root.find('filename').text = save_title + '.jpg'
    root.find('path').text = img_save_path
    tree.write(xml_save_path)

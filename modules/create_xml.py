import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import random
import os
import cv2

SAMPLE_XML_PATH = '/Users/chiang-en/Documents/projects/tbrain/sample_prime.xml'
TRAIN_INFO_PATH = '/Users/chiang-en/Documents/projects/tbrain/標記與資料說明 2/public_training_data.csv'
TEST_INFO_PATH = '/Users/chiang-en/Documents/projects/tbrain/標記與資料說明 2/public_testing_data.csv'

def toXml(img_folder, img_name, img_format, xmin_v, xmax_v, ymin_v, ymax_v,sample_xml_path = SAMPLE_XML_PATH):
    '''
        ex.
        img_folder = '/Users/chiang-en/Documents/projects/tbrain/public_training_data/'
        img_name = 'IxUp4myw5e6YDH6jNocwvtCE9yC9JM1'
        img_format = '.jpg'
        xmin, xmax, ymin, ymax = 1, 2, 3, 4
    '''
    tree = ET.parse(sample_xml_path)
    root = tree.getroot()
    folder = root.find('folder')
    filename = root.find('filename')
    path = root.find('path')
    obj = root.find('object')
    bndbox = obj.find('bndbox')
    xmin, xmax = bndbox.find('xmin'), bndbox.find('xmax')
    ymin, ymax = bndbox.find('ymin'), bndbox.find('ymax')
    # print(xmin.text)
    # change some values
    folder.text = img_folder
    filename.text = img_name + img_format
    path.text = img_folder + img_name + img_format
    xmin.text, xmax.text = str(xmin_v), str(xmax_v)
    ymin.text, ymax.text = str(ymin_v), str(ymax_v)
    
    # write and return the new xml
    # print(img_name)
    xml_save_path = img_folder + img_name + '.xml'
    # print(xml_save_path)
    tree.write(xml_save_path)
    return tree


def batch_toXml(img_folder, img_format, sample_xml_path = SAMPLE_XML_PATH,info_path = TRAIN_INFO_PATH):
    info_df = pd.read_csv(info_path)
    for i in range(info_df.shape[0]):
        img_name = info_df['filename'].values[i]
        tl_x, tl_y = info_df['top left x'].values[i], info_df['top left y'].values[i]
        tr_x, tr_y = info_df['top right x'].values[i], info_df['top right y'].values[i]
        bl_x, bl_y = info_df['bottom left x'].values[i], info_df['bottom left y'].values[i]
        br_x, br_y = info_df['bottom right x'].values[i], info_df['bottom right y'].values[i]

        xmin_v, xmax_v = min(tl_x, bl_x), max(tr_x, br_x)
        ymin_v, ymax_v = min(tl_y, tr_y), max(bl_y, br_y)

        toXml(img_folder, img_name, img_format, xmin_v, xmax_v, ymin_v, ymax_v, sample_xml_path)

        

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
            



def pathching(sample_xml_path = SAMPLE_XML_PATH, save_name_title = '', save_folder = ''):
    # parameters
    char_main_folder = '/Users/chiang-en/Documents/projects/tbrain/digits_1011/'
    chars = [str(i) for i in range(10)] + ['A','B','C','D','E','F','G','H','J','K','L','M','N','P','Q','R','S','T','U','V','W','X','Y','Z']
    bg_ref = np.zeros((1028, 1232, 3),dtype='uint8')
    bg_patching = np.zeros((1028, 1232, 3),dtype='uint8')
    
    # read the sample xml
    tree = ET.parse(sample_xml_path)
    root = tree.getroot()

    # 
    random.shuffle(chars)
    for char in chars:
        img_folder = char_main_folder + char + '/'
        img_names = os.listdir(img_folder)
        random_ind = random.randint(0, len(img_names) - 1)
        img_path = img_folder + img_names[random_ind]
        img = cv2.imread(img_path, 1)
        #ai. add img
        bg_now = np.zeros((1028, 1232, 3),dtype='uint8')
        indicator = np.ones(img.shape, dtype='uint8')
        width, height = indicator.shape[1], indicator.shape[0]
        random_x = random.randint(0, bg_now.shape[1] - width - 2)
        random_y = random.randint(0, bg_now.shape[0] - height - 2)

        bg_now[random_y:random_y + height, random_x:random_x + width, :] = indicator

        if (bg_now*bg_ref).sum()>0:
            continue
        else:
            # step 1. patching
            bg_patching[random_y:random_y+height, random_x:random_x+width, :] = img

            # step 2. update bg_ref
            bg_ref[random_y:random_y + height, random_x:random_x + width, :] = indicator
            
            # step 3. add an object into xml
            xmin, ymin = str(random_x), str(random_y)
            xmax, ymax = str(random_x + width - 1), str(random_y + height - 1) 
            new_element = create_an_object(char, xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)
            root.insert(6, new_element)

        # add rimg
        bg_now = np.zeros((1028, 1232, 3),dtype='uint8')
        random_x = random.randint(0, bg_now.shape[1] - width - 2)
        random_y = random.randint(0, bg_now.shape[0] - height - 2)
        bg_now[random_y:random_y + height, random_x:random_x + width, :] = indicator

        if (bg_now*bg_ref).sum()>0:
            continue
        else:
            rimg = cv2.rotate(img, cv2.ROTATE_180)
            # step 1. patching
            bg_patching[random_y:random_y+height,random_x:random_x+width, :] = rimg

            # step 2. update bg_ref
            bg_ref[random_y:random_y + height, random_x:random_x + width, :] = indicator

            # step 3. add an object into xml
            xmin, ymin = str(random_x), str(random_y)
            xmax, ymax = str(random_x + width - 1), str(random_y + height - 1)
            if char=='0' or char=='8' or char=='S' or char=='Z' or char=='H' or char=='N' or char=='X':
                new_element = create_an_object(char, xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)
            else:
                new_element = create_an_object('-'+char, xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

            root.insert(6, new_element)

    # save img and xml
    img_save_path = save_folder + save_name_title + '.jpg'
    cv2.imwrite(img_save_path, bg_patching)
    xml_save_path = save_folder + save_name_title + '.xml'
    root.find('filename').text = save_name_title + '.jpg'
    root.find('path').text = img_save_path
    tree.write(xml_save_path)


    

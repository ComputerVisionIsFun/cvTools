import xml.etree.ElementTree as ET
import numpy as np
import random
import os
import cv2


def create_xml(folder, filename, objs, sample_xml_path, new_xml_save_path, img_w, img_h, img_d,obj_name):
    '''
    objs = [obj0, obj1, ...], where obji = [[xmin,ymin], [], [xmax,ymax], []]

    '''
    # read xml
    tree = ET.parse(sample_xml_path)
    root = tree.getroot()
    # assign folder, filename, path
    root.find('folder').text = folder
    root.find('filename').text = filename
    root.find('path').text = folder + filename
    
    # assign width and height
    root.find('size').find('width').text = str(int(img_w))
    root.find('size').find('height').text = str(int(img_h))
    root.find('size').find('depth').text = str(int(img_d))

    # create objs
    for obj in objs:
        print(obj[0][0],'\n')
        xmin, ymin = str(obj[0][0][0]), str(obj[0][0][1])
        xmax, ymax = str(obj[0][2][0]), str(obj[0][2][1]) 
        new_element = create_an_object(obj_name, xmin, ymin, xmax, ymax)
        root.insert(6, new_element)

    # write to a new xml
    tree.write(new_xml_save_path)



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
        ET.SubElement(new_element[4], ele)#add ele in {xmin, xmax, ymin, ymax} to new_element[4]=bndbox
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
    root.find('filename').text = save_title + save_img_format
    root.find('path').text = img_save_path
    tree.write(xml_save_path)        


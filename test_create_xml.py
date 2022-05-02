from modules import create_xml as cx
import easyocr
import os
import cv2


sample_xml_path = 'sample.xml'
img_folder = 'D:/Dataset/Lpr_2nd/'
img_filename = '2.png'

files = os.listdir(img_folder)
clean_files = []
for file in files:
    if file[-1]=='g':
        clean_files.append(file)

reader = easyocr.Reader(['en'])
for file in clean_files:
    img = cv2.imread(img_folder + file, 1)

    objs = reader.readtext(img_folder + file)
    if len(objs)==0:
        continue
    
    new_xml_save_path = img_folder + file.replace('png','') + 'xml'
    cx.create_xml(img_folder,img_filename,objs,sample_xml_path,new_xml_save_path,img.shape[1],img.shape[0],3,'plate')







# objs = [([[115, 287], [226, 287], [226, 336], [115, 336]],'985 E6', 0.34893422936299495),([[983, 283], [1077, 283], [1077, 347], [983, 347]],'13$5',0.7898624539375305)]

# print('---',objs[0][0])


# new_xml_save_path = img_folder + img_filename.replace('png','') + 'xml'

# cx.create_xml(img_folder,img_filename,objs,sample_xml_path,new_xml_save_path,1280,720,3,'plate')
from modules import create_xml as cx

sample_xml_path = '/Users/chiang-en/Documents/GitHub/cvTools/sample.xml'
img_folder = '/Users/chiang-en/Documents/GitHub/cvTools/create_xml_test/'
img_filename = '2.png'

objs = [([[115, 287], [226, 287], [226, 336], [115, 336]],'985 E6', 0.34893422936299495),([[983, 283], [1077, 283], [1077, 347], [983, 347]],'13$5',0.7898624539375305)]

print('---',objs[0][0])


new_xml_save_path = img_folder + img_filename.replace('png','') + 'xml'

cx.create_xml(img_folder,img_filename,objs,sample_xml_path,new_xml_save_path,1280,720,3,'plate')
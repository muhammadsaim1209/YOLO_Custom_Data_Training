
import os
from os import getcwd
import numpy as np
import cv2

def convert(size, x, y, w, h):
    box = np.zeros(4)
    dw = 1./size[0]
    dh = 1./size[1]
    x = x / dw
    w = w / dw
    y = y / dh
    h = h / dh
    box[0] = x - (w / 2.0)
    box[1] = x + (w / 2.0)
    box[2] = y - (h / 2.0)
    box[3] = y + (h / 2.0)
    return box
    
"""-------------------------------------------------------------------""" 

""" Configure Paths"""   
label_path = "Annotations_YOLO/HCM/test/1000x"  
image_path = "Dataset_Final/LOlympus/test/1000x"      
output_path = "YOLO_Plot/LOlympus/test/1000x"    
if not os.path.exists(output_path):
        os.makedirs(output_path)
wd = getcwd()

""" Get yolo txt file list """
txt_list = []
for file in os.listdir(label_path):
    if file.endswith(".txt"):
        txt_list.append(file)
    

""" Process """
for txt_name in txt_list:
    img_filename = txt_name.rstrip(".txt") + "x.png"
    img_path = os.path.join(image_path, img_filename)
    img = cv2.imread(img_path)

    """ Open input text files """
    txt_path = os.path.join(label_path, txt_name)
   # print("Input:" + txt_path)
    txt_file = open(txt_path, "r")
    
    img_outpath = os.path.join(output_path, img_filename)
    #print("Output:" + img_outpath)

    """ Convert YOLO format to get xmin, ymin, xmax, ymax """ 
    lines = txt_file.read().splitlines()  
    for idx, line in enumerate(lines):
        value = line.split()
        x = float(value[1])
        y = float(value[2])
        w = float(value[3])
        h = float(value[4])
	
        img_h, img_w = img.shape[:2]
        bb = convert((img_w, img_h), x, y, w, h)
        cv2.rectangle(img, (int(round(bb[0])), int(round(bb[2]))),
                      (int(round(bb[1])), int(round(bb[3]))), (0, 0, 255), 2)
        # Uncomment to show label index
        # cv2.putText(img, value[0], (int(round(bb[0])), int(round(bb[2]))-10), 
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)      
    cv2.imwrite(img_outpath, img)

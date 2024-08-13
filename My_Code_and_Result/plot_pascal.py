import os
import xml.etree.ElementTree as ET
import cv2

def convert_pascal_voc(size, box):
    """Convert Pascal VOC box format to xmin, ymin, xmax, ymax."""
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = box[0] * dw
    w = box[1] * dw
    y = box[2] * dh
    h = box[3] * dh
    return (int(x), int(y), int(x + w), int(y + h))

"""-------------------------------------------------------------------""" 

""" Configure Paths"""   
annotation_path = "Annotations/HCM/test/1000x"
image_path = "Dataset_Final/LOlympus/test/1000x"      
output_path = "Pascal_Plot/LOlympus/test/1000x"    

if not os.path.exists(output_path):
    os.makedirs(output_path)

""" Get Pascal VOC xml file list """
xml_list = [f for f in os.listdir(annotation_path) if f.endswith('.xml')]

""" Process """
for xml_name in xml_list:
    img_filename = xml_name.replace(".xml", ".png")
    img_path = os.path.join(image_path, img_filename)
    img = cv2.imread(img_path)

    """ Parse XML file """
    xml_path = os.path.join(annotation_path, xml_name)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    img_h, img_w = img.shape[:2]

    for obj in root.findall('object'):
        bbox = obj.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)

        # Draw rectangle on image
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
        
        # Uncomment to show label index
        # label = obj.find('name').text
        # cv2.putText(img, label, (xmin, ymin-10), 
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    img_outpath = os.path.join(output_path, img_filename)
    cv2.imwrite(img_outpath, img)

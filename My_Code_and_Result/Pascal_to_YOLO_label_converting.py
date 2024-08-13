import os
import xml.etree.ElementTree as ET
def class_name_to_id(class_name):
    # This function should map your class names to integer IDs
    # Modify this according to your dataset's class names and IDs
    classes = {'gametocyte': 0, 'schizont': 1, 'trophozoite': 2, 'ring':3}  # Add your own classes
    return classes.get(class_name, -1)

def convert_voc_to_yolo(label_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for label_file in os.listdir(label_dir):
        if not label_file.endswith('.xml'):
            continue

        # Parse the XML file
        tree = ET.parse(os.path.join(label_dir, label_file))
        root = tree.getroot()

        # Get image dimensions
        size = root.find('size')
        img_width = int(size.find('width').text)
        img_height = int(size.find('height').text)

        # Create the output YOLO label file
        output_file = os.path.join(output_dir, label_file.replace('.xml', '.txt'))
        with open(output_file, 'w') as out_f:
            for obj in root.findall('object'):
                # Get the class label
                class_name = obj.find('name').text
                # Get the class ID (in YOLO format, this should be an integer starting from 0)
                class_id = class_name_to_id(class_name)

                # Get the bounding box coordinates
                bndbox = obj.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)

                # Convert to YOLO format
                x_center = (xmin + xmax) / 2.0 / img_width
                y_center = (ymin + ymax) / 2.0 / img_height
                width = (xmax - xmin) / float(img_width)
                height = (ymax - ymin) / float(img_height)

                # Write the YOLO label
                out_f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")


# Example usage
label_dir = 'Annotations/LCM/val/1000x'
output_dir = 'Annotations_YOLO/LCM/val/1000x'
convert_voc_to_yolo(label_dir, output_dir)
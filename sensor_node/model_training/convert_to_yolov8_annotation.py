import json
import os
import shutil

def convert_to_yolo(json_path, output_dir, no_bbox_dir, class_mapping):
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)

    if not os.path.exists(no_bbox_dir):
        os.mkdir(no_bbox_dir)

    for image_data in data['images']:
        image_path = image_data['file']
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        # Only create txt file for images with bounding boxes
        if len(image_data['detections']) > 0:
            output_path = os.path.join(output_dir, f"{image_name}.txt")
        else: # Move images without bounding boxes into a seperate folder
            shutil.move(os.path.join(output_dir, f"{image_name}.jpg"), os.path.join(no_bbox_dir, f"{image_name}.jpg"))

        with open(output_path, 'w') as output_file:
            for detection in image_data['detections']:
                class_label = detection['category']

                if class_label == "1": # 1 is animals in Megadetector
                    bbox = detection['bbox']

                    # convert to YOLOv8 annotation
                    bbox_left = bbox[0]
                    bbox_top = bbox[1]
                    width = bbox[2]
                    height = bbox[3]
                
                    x_center = bbox_left + width / 2
                    y_center = bbox_top + height / 2

                    output_line = f"{class_mapping} {round(x_center,6)} {round(y_center,6)} {round(width,6)} {round(height,6)}\n"
                    output_file.write(output_line)

# Usage
json_path = f"/data/dog_train.json"
output_dir = f"/data/input/data/train/Dogs"
no_bbox_dir = f"/data/train/Dogs/noBBox"
class_mapping = 1  # 0 for Cats, 1 for Dogs

convert_to_yolo(json_path, output_dir, no_bbox_dir, class_mapping)
import ultralytics
ultralytics.checks()
from ultralytics import YOLO
import os
import cv2
import time 
# import shutil
# import argparse
import configparser

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')
database_path = config['DEFAULT']['database_path'] 
database_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), database_path)

def load_model():
    print ('************* loading YOLO model... *************')

    # Code to load the model
    model_detect = YOLO("weights/best_detect.pt")
    print ('************* model YOLO loaded *************')
    return model_detect

def get_bbox(filepath, model_detect):
    print (f"YOLO SERVER Processing image {filepath} ")
    save_folder = f'{database_path}/yolo_output/{os.path.basename(filepath)}'
    os.makedirs(save_folder, exist_ok=True)
    img = cv2.imread(filepath)
    model_detect = YOLO("weights/best_detect.pt")
    print ('model detect YOLLOOOOOO: ', model_detect)
    result = model_detect(filepath, conf = 0.542)  # return a list of Results objects
    # Process results list
    print ('YOLO have detected ', len(result[0].boxes), ' objects')
    boxes = result[0].boxes.xyxy.tolist()
    boxes_sorted = sorted(boxes, key=lambda x: x[0])
    for index, box in enumerate(boxes_sorted):
        x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        crop_img = img[y1:y2, x1:x2]
        crop_img = cv2.resize(crop_img, (640, 640))
        cv2.imwrite(os.path.join(save_folder, f'{index}.jpg'), crop_img)
    return save_folder 

def process_image(image_path, model):
    # Code to process the image
    # image got from api -> yolo image -> ocr image -> return ocr output 
    print(f"YOLO SERVER Processing image {image_path} ")
    filepath = image_path
    img = cv2.imread(filepath)
    img = cv2.resize(img, (640, 640))
    new_filepath = filepath.replace('.', '_resized.')
    cv2.imwrite(new_filepath, img)
    time.sleep(1)
    save_folder = get_bbox(new_filepath, model)
    print ("YOLO SERVER DONE")
    return save_folder

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--load_model", action="store_true", help="Load the model")
#     parser.add_argument("--process_image", type=str, help="Path to the image to process")
#     args = parser.parse_args()

#     if args.load_model:
#         load_model()
#     if args.process_image:
#         result = process_image(args.process_image)
#         print(result)






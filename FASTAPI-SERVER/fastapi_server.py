from fastapi import FastAPI, HTTPException, File, UploadFile
import requests
import uuid
import os 
import uvicorn
from PIL import Image
import io
import logging
# Configure logging to a file
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='fastapi.log', filemode='w')

logger = logging.getLogger(__name__)

import configparser

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')
database_path = config['DEFAULT']['database_path'] 


app = FastAPI()

ocr_service_address = '0.0.0.0'
yolo_service_address = '0.0.0.0'
yolo_service_port = 8001
ocr_service_port = 8002
save_directory = f'{database_path}/yolo_input'
# Endpoint to receive an image and start the processing pipeline
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/ping_yolo")
async def ping_yolo():
    response = requests.get(f"http://{yolo_service_address}:{yolo_service_port}/")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="YOLO SERVER OFFLINE")
    else:
        return {"message": response.text}

@app.get("/ping_ocr")
async def ping_ocr():
    response = requests.get(f"http://{ocr_service_address}:{ocr_service_port}/")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="OCR SERVER OFFLINE")
    else:
        return {"message": response.text}

@app.get("/load_model_yolo")
async def load_model_yolo():
    response = requests.get(f"http://{yolo_service_address}:{yolo_service_port}/load_model")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="CANNOT LOAD YOLO MODEL")
    else:
        return {"message": response.text}

@app.get("/load_model_ocr")
async def load_model_ocr():
    response = requests.get(f"http://{ocr_service_address}:{ocr_service_port}/load_model")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="CANNOT LOAD OCR MODEL")
    else:
        return {"message": response.text}
    
@app.post("/process-image")
async def process_image(file: UploadFile = File(...)):
    request_object_content = await file.read()
    unique_id = str(uuid.uuid4())
    file_path = os.path.join(save_directory, f"{unique_id}.jpg")

    # Ensure the save directory exists
    os.makedirs(save_directory, exist_ok=True)

    # Save the image file
    img = Image.open(io.BytesIO(request_object_content))
    # Save the image to a file
    img.save(file_path)
    print ('*********** GOT IMAGE ***********')

    # Send the image content to YOLO service
    response = requests.post(f"http://{yolo_service_address}:{yolo_service_port}/run", json={"file": file_path})
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="YOLO Detection failed")

    detected_objects = response.json()

    # Send the detected objects to OCR service
    ocr_results = requests.post(f"http://{ocr_service_address}:{ocr_service_port}/run", json=detected_objects)
    if ocr_results.status_code != 200:
        raise HTTPException(status_code=500, detail="OCR processing failed")
    ocr_results = ocr_results.json()
    return {"id": unique_id, 'ocr_result': ocr_results["ocr_result"]}

def main():
    print ('INITIALIZING FASTAPI SERVER')
    uvicorn.run("fastapi_server:app", host="10.0.68.103", port=8004, reload=True)

if __name__ == "__main__":
    main()

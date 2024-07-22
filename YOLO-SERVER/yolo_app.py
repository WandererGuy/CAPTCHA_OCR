from fastapi import FastAPI, HTTPException, Request
from main_yolo import load_model, process_image
import uvicorn
import os 
from typing import Optional

app = FastAPI()
model = None 

import configparser

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')
database_path = config['DEFAULT']['database_path'] 
ocr_service_address = config['DEFAULT']['ocr_service_address']
yolo_service_address = config['DEFAULT']['yolo_service_address']
yolo_service_port = int(config['DEFAULT']['yolo_service_port'])
ocr_service_port = int(config['DEFAULT']['ocr_service_port'])
fastapi_service_port = int(config['DEFAULT']['fastapi_service_port'])
host_ip = config['DEFAULT']['host_ip']

database_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), database_path)

def load_model_yolo_once():
    print ('************* loading YOLO model... *************')
    global model
    model = load_model()
    return {"message": "YOLO model loaded"}

@app.get("/")
async def root():
    return {"message": "YOLO service is up and runnin"}

@app.get("/load_model")
async def load_model_yolo():
    print ('************* loading YOLO model... *************')
    global model
    model = load_model()
    print ('1 variation model: ', model)
    return {"message": "YOLO model loaded"}


@app.api_route("/run", methods = ["GET","POST"])
async def detect(request: Request, data: Optional[dict] = None):
    if request.method == "GET":
        return {"message": "YOLO service is ready"}
    if request.method == "POST":
        file_path = data['file']
        print (file_path)
        try:
            if model != None :
                print ('model existed')
            save_folder = process_image(file_path, model)
            print ("YOLO SERVER DONE DETECTION")
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        return {"message": "Detection completed", "save_folder": save_folder}

@app.on_event("startup")
async def startup_event():
    load_model_yolo_once()
    print ('loaded model')



def main():
    print ('INITIALIZING YOLO SERVER')
    os.makedirs(f'{database_path}/yolo_output', exist_ok=True)
    print(f"Directory {database_path}/yolo_output created successfully")
    uvicorn.run("yolo_app:app", host=host_ip, port=yolo_service_port, reload=True)

if __name__ == "__main__":
    main()
    
    
    
    

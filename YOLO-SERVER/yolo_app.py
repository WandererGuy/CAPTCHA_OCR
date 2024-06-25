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
        try:
            print ('model 2', model)
            save_folder = process_image(file_path, model)
            print ("YOLO SERVER DONE DETECTION")
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        return {"message": "Detection completed", "save_folder": save_folder}

def main():
    print ('INITIALIZING YOLO SERVER')
    try:
        os.makedirs(f'{database_path}/yolo_output', exist_ok=True)
        print(f"Directory {database_path}/yolo_output created successfully")
    except Exception as e:
        print(f"Error creating directory: {e}")

    os.makedirs(f'{database_path}/yolo_output', exist_ok = True)
    uvicorn.run("yolo_app:app", host="0.0.0.0", port=8001, reload=True)

if __name__ == "__main__":
    main()
    
    
    
    

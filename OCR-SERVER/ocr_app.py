from fastapi import FastAPI, HTTPException
from main_ocr import ocr, load_model
import uvicorn
import os 
import configparser
import traceback 

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


app = FastAPI()
model = None 

def load_model_ocr_once():
    print ('************* loading OCR model... *************')
    global model
    model = load_model()
    return {"message": "OCR model loaded"}


@app.get("/")
async def root():
    return {"message": "OCR service is up and runnin"}

@app.get("/load_model")
async def load_model_ocr():
    print ('************* loading OCR model... *************')
    global model
    model = load_model()
    return {"message": "OCR model loaded"}

@app.post("/run")
async def detect(data: dict):
    global model
    folder_path = data['save_folder']
    try:
        output = ocr(folder_path, model)
    except Exception as e:
        traceback.print_exc()  # In chi tiết lỗi ra terminal
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}\n{error_trace}")


    return {"message": "OCR completed", "ocr_result": output}

@app.on_event("startup")
async def startup_event():
    print ('INITIALIZING OCR SERVER')
    load_model_ocr_once()
    print ('loaded model')

def main():
    uvicorn.run("ocr_app:app", host=host_ip, port=ocr_service_port, reload = True)

if __name__ == "__main__":
    main()
    
    
    

from fastapi import FastAPI, HTTPException
from main_ocr import ocr, load_model
import uvicorn
import os 

app = FastAPI()
model = None 

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
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "OCR completed", "ocr_result": output}

def main():
    print ('INITIALIZING OCR SERVER')
    uvicorn.run("ocr_app:app", host="0.0.0.0", port=8002, reload = True)

if __name__ == "__main__":
    main()
    
    
    

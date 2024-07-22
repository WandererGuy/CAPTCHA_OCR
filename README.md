## description 
this is a automnate text-based Captcha solver (yolov8 trained on captcha collected from https://hashes.com/en/decrypt/hash)

## usage
Step 1 : git clone this repo  <br>
Step 2: prepare 3 different environments for FASTAPI-SERVER, YOLO-SERVER, OCR-SERVER <br>
### FASTAPI 
```
conda create -p D:\ManhT04\CAPTCHA_OCR\FASTAPI-SERVER\env_fast_api python==3.9
conda activate D:\ManhT04\CAPTCHA_OCR\FASTAPI-SERVER\env_fastapi
pip install fastapi uvicorn pillow requests uuid=
```

### YOLO 
```
conda create -p D:\ManhT04\CAPTCHA_OCR\YOLO-SERVER\env_yolo python==3.9
conda activate D:\ManhT04\CAPTCHA_OCR\YOLO-SERVER\env_yolo
pip install ultralytics
pip install fastapi uvicorn opencv-python
```

### OCR (my max CUDA support is 11.3)
```
conda create -p D:\ManhT04\CAPTCHA_OCR\OCR-SERVER\env_ocr python==3.9
conda activate D:\ManhT04\CAPTCHA_OCR\OCR-SERVER\env_ocr
conda install pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cudatoolkit=11.3 -c pytorch
pip install fastapi uvicorn pillow
pip install vietocr==0.3.12
```
<br>
Step 3: fix path for env in 3 init.sh file in FASTAPI-SERVER, YOLO-SERVER, OCR-SERVER to match your created env<br>

Small note: <br>
You send http POST request (which is the image you want to get OCR) to app in FASTAPI_server (see FASTAPI-SERVER/fastapi_server.py to understand) <br>
Inside, FASTAPI_server send image to YOLO server . After that YOLO send results to OCR server. <br>
After that, OCR send final result to FASTAPI server. Finally FASTAPI server send back message to you , which is the OCR output.<br> 

Step 4: turn on each server , each activated on 1 terminal, so you need 3 terminals , then run app script of it <br>

Method:<br>
Yolov8 outputs separate character as images, then VietOCR will OCR that image and give output <br>
You can improve this based on your Captcha, by finetune my Yolov8 weight (see more on ultralytics yolov8 website for finetune)<br>





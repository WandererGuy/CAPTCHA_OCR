## description 
this is a automnate text-based Captcha solver (yolov8 trained on captcha collected from https://hashes.com/en/decrypt/hash)

## usage
Step 1 : git clone this repo  <br>
Step 2: prepare 3 different environments for FASTAPI-SERVER, YOLO-SERVER, OCR-SERVER <br>
for FASTAPI:
  - conda create --name env_fastapi python==3.9
  - conda activate env_fast_api
    then you can install fastapi, uvicorn, pillow, requests, uuid, logging, io (should check for conda package before check for pip install)
for YOLO:
  - conda create --name env_yolo python==3.9
  - conda activate env_yolo
  - pip install ultralytics

for OCR-SERVER:
  - conda create --name env_ocr python==3.9
  - conda activate env_ocr
  - conda install pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cudatoolkit=11.3 -c pytorch (this torch suits my machine , which support max CUDA 11.3)
  - pip install vietocr==0.3.12
    then you can install fastapi,uvicorn, pillow

Step 3: fix path for env in 3 init.sh file in FASTAPI-SERVER, YOLO-SERVER, OCR-SERVER to match your created env<br>

Step 4:<br>
Change host value in line 99 of FASTAPI-SERVER/fastapi_server.py to your IP address. <br> 
Small note: 
You send http POST request (which is the image you want to get OCR) to app in FASTAPI_server (see FASTAPI-SERVER/fastapi_server.py to understand) <br>
Inside, FASTAPI_server send image to YOLO server . After that YOLO send results to OCR server. <br>
After that, OCR send final result to FASTAPI server. Finally FASTAPI server send back message to you , which is the OCR output.<br> 

Step 5: turn on each server , each activated on 1 terminal, so you need 3 terminals <br>
- In first terminal<br>
cd FASTAPI-SERVER<br>
bash init.sh<br>
- In second terminal<br>
cd YOLO-SERVER<br>
bash init.sh<br>
- In third terminal<br>
cd OCR-SERVER<br>
bash init.sh<br>
<br>
Method:<br>
Yolov8 outputs separate character as images, then VietOCR will OCR that image and give output <br>
You can improve this based on your Captcha, by finetune my Yolov8 weight (see more on ultralytics yolov8 website for finetune)<br>

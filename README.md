## description 
this is a automnate text-based Captcha solver (yolov8 trained on captcha collected from https://hashes.com/en/decrypt/hash)

## usage
Step 1 : git clone this repo  <br>
Step 2 : turn on each server , each activated on 1 terminal, so you need 3 terminals <br>
- In first terminal<br>
cd FASTAPI_server<br>
bash init.sh<br>
- In second terminal<br>
cd YOLO_server<br>
bash init.sh<br>
- In third terminal<br>
cd OCR_server<br>
bash init.sh<br>

Step 3:<br>
you send http POST request (which is the image you want to get OCR) to app in FASTAPI_server<br>
Inside, FASTAPI_server send image to YOLO server . After that YOLO send results to OCR server. <br>
After that, OCR send final result to FASTAPI server. Finally FASTAPI server send back message to you , which is the OCR output.<br> 

Method:<br>
Yolov8 outputs separate character as images, then VietOCR will OCR that image and give output <br>
You can improve this based on your Captcha, by finetune my Yolov8 weight (see more on ultralytics yolov8 website for finetune)<br>

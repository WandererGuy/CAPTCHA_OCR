#!/bin/bash

# Activate the Conda environment
source /home/ai-ubuntu/anaconda3/etc/profile.d/conda.sh
eval "$(conda shell.bash hook)"
conda activate /home/ai-ubuntu/hddnew/Manh/CAPTCHA_OCR/OCR-SERVER/env_ocr


# Run the Python script
# Check if the environment was activated
if [[ $? -ne 0 ]]; then
    echo "Failed to activate Conda environment."
    exit 1
fi

echo "Conda environment activated."

# Run the Python script
python /home/ai-ubuntu/hddnew/Manh/CAPTCHA_OCR/OCR-SERVER/ocr_app.py

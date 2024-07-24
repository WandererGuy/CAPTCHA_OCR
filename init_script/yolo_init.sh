#!/bin/bash

# Đọc đường dẫn từ tập tin cấu hình
CONFIG_FILE="init_script/config.ini"
# Sử dụng lệnh grep và cut để lấy giá trị từ tập tin cấu hình
CONDA_PATH=$(grep 'conda_path' "$CONFIG_FILE" | cut -d' ' -f3)
echo "found config file"
SERVER_PATH=$(pwd)


# Kích hoạt Conda
source "$CONDA_PATH"
eval "$(conda shell.bash hook)"

# Kích hoạt môi trường Conda
conda activate "$SERVER_PATH/YOLO-SERVER/env_yolo"

# Kiểm tra xem môi trường có được kích hoạt thành công không
if [[ $? -ne 0 ]]; then
    echo "Failed to activate Conda environment."
    exit 1
fi

echo "Conda environment activated."

cd "$SERVER_PATH/YOLO-SERVER"
# Chạy script Python
python yolo_app.py

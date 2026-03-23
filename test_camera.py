import common.capture
import time
import common.handler
import os
from pathlib import Path

cammond = common.capture.AdbCmd()

def test_aspect_ratio():
    cammond.delete_files("/sdcard/DCIM/Camera/*")
    time.sleep(2)
    cammond.start_app("com.motorola.camera5", "com.motorola.camera.Camera")
    time.sleep(5)
    cammond.tap(593, 2370)
    time.sleep(20)
    
    # 获取图片名称
    img_name = cammond.get_img_name("/sdcard/DCIM/Camera")
    print(f"Image name: '{img_name}'")  # 调试打印
    
    # 检查是否成功获取文件名
    if not img_name:
        raise ValueError("Failed to get image name from device")
    
    # 创建本地目录
    Path("Camera").mkdir(exist_ok=True)
    
    # 拉取文件
    local_path = f"Camera/{img_name}"
    cammond.pull_file(f"/sdcard/DCIM/Camera/{img_name}", local_path)
    time.sleep(2)
    
    print("File saved successfully.")
    
    # 验证文件存在
    if not Path(local_path).exists():
        raise FileNotFoundError(f"File not found: {local_path}")
    
    handler = common.handler.ImageHandler(local_path)
    print(handler.get_shape(), img_name)
    aspect_ratio = handler.get_shape()[1] / handler.get_shape()[0]
    assert aspect_ratio == 4/3, f"Expected aspect ratio 4:3, but got {aspect_ratio:.2f}"
    os.remove(local_path)  # 清理测试生成的文件


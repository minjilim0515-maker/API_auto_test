from importlib.resources import path
from time import sleep

import cv2

class ImageHandler:
    def __init__(self, img_path):
        self.img_path = img_path
        self.img = None

    def load_image(self):
        self.img = cv2.imread(self.img_path)
        if self.img is None:
            raise ValueError(f"Could not load image from {self.img_path}")
        return self.img

    def display_image(self):
        if self.img is None:
            self.load_image()
        cv2.imshow("Display window", self.img)
       
    def get_shape(self, img=None):
        """获取图像shape，如果不传img则使用self.img"""
        if img is None:
            if self.img is None:
                self.load_image()
            return self.img.shape
        else:
            return img.shape
    
    def save_image(self, output_path):
        if self.img is None:
            self.load_image()
        cv2.imwrite(output_path, self.img)
        print(f"Image saved to {output_path}")

    def img_to_gray(self):
        if self.img is None:
            self.load_image()
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        return self.img
    
    def img_to_binary(self, threshold=127):
        if self.img is None:
            self.load_image()
        _, binary_img = cv2.threshold(self.img, threshold, 255, cv2.THRESH_BINARY)
        return binary_img

# 使用封装的类

# handler.display_image()


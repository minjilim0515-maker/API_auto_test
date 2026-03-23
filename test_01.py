from common.handler import ImageHandler
import pytest
import os

@pytest.fixture(scope="module")
def handler():
    return ImageHandler('test.jpg')

def test_img_shape(handler):
    assert handler.get_shape() == (536, 536, 3)  # 实际待替换

def test_save_image(handler):
    output_path = 'output.jpg'
    handler.save_image(output_path)
    assert os.path.exists(output_path)
    os.remove(output_path)  # 清理测试生成的文件

def test_img_to_gray(handler):
    gray_img = handler.img_to_gray()
    assert len(gray_img.shape) == 2  # 灰度图应该只有两个维度
    handler.save_image('gray_output.jpg')
    print(handler.get_shape(gray_img))


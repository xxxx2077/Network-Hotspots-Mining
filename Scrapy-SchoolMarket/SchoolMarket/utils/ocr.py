from paddleocr import PaddleOCR
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# 可以根据需要进行配置
# 使用方向分类器（识别非水平方向的文字），中文，不打印日志信息
ppocr = PaddleOCR(use_angle_cls=True, lang="ch",show_log=False)


import requests
from PIL import Image
from io import BytesIO
import numpy as np

# 返回PIL.Image对象
def download_image(url):
    response = requests.get(url, stream=True)
    # 不成功则抛出异常
    response.raise_for_status()
    return Image.open(BytesIO(response.content))

def save_image(image:Image, save_path='tmp.jpg'):    
    image = image.convert('RGB')
    image.save(save_path)
    return save_path

def load_image(image_path='tmp.jpg'):
    return Image.open(image_path).convert('RGB')

def convert_pil_to_np(image:Image):
    image = image.convert('RGB')
    return np.array(image)


    
def ocr_img_from_url(url, save_path='tmp.jpg',save=False, ocr=ppocr):
    image = download_image(url)
    # ppocr支持ndarray类型
    image_np = convert_pil_to_np(image)
    result = ocr.ocr(image_np, cls=True)
    # 可以保存图片留待查看
    if save:
        save_image(image, save_path)
    return result

def ocr_img_from_local(path='tmp.jpg',ocr=ppocr):
    # ppocr支持ndarray,图片路径，不支持PIL.Image
    result = ocr.ocr(path,cls=True)
    return result


if __name__ == "__main__":
    # result = ocr.ocr('../tmp.jpg', cls=True)
    # print(result[0][0])
    url = "https://b1.cdn.zanao.com/upload/2024/05/13/tvbpdyg2dubjnqm.jpeg@!common"
    print(ocr_img_from_url(url=url,save=True))
    # print(ocr_img_from_local())

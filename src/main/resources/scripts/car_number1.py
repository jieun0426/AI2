import cv2
import easyocr
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import requests
import json
import os

# 이미지 파일 경로 설정
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
image_path = os.path.join(project_root, "data", "temp_carnumber_image.jpg")


# 이미지 로딩
img = cv2.imread(image_path)
if img is None:
    raise FileNotFoundError(f"이미지를 찾을 수 없습니다: {image_path}")

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# EasyOCR
reader = easyocr.Reader(['ko', 'en'])
results = reader.readtext(img_rgb)


for (bbox, text, prob) in results:
    # OCR 결과 x좌표 기준 정렬
    results_sorted = sorted(results, key=lambda x: x[0][0][0])  # bbox 왼쪽 위 점의 x좌표 기준
    number_plate_text = "".join([r[1] for r in results_sorted])

data={
    "text": number_plate_text,
    "prob": prob
}

url="http://localhost:1820/python/numberout"

response=requests.post(url, json=data)

print(response.text)

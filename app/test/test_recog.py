import pytest
from app.recog import ImageRecognition
import cv2
import json


def test_recognition():
    ir = ImageRecognition()
    
    img = cv2.imread('app/test/channel1_2018Sep02095048_30.jpg')

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #grayscale
    img,h,w = ir.resize_image(img)

    json_response = json.loads(ir.get_ocr_as_json(img))
    assert(json_response.get('clean_ocr') == 'PK-GIF')
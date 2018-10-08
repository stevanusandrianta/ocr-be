import os
import cv2
import numpy
import json

from flask import Flask, flash, request
from app.recog import ImageRecognition

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

APP = Flask(__name__)
ir = ImageRecognition()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@APP.route('/mock/ocr')
def mock_ocr():
    return """
        {"ocr": ". PK\u2014GIF \u2018\n, a\nV . uuuuuuu (Li 00\u00a2", "clean_ocr": "PK-GIF", "bounding_boxes": 
        [". 43 474 45 476 0", "P 1025 363 1049 393 0", "K 1050 357 1073 387 0", "\u2014 1079 362 1094 367 0", "G 1104 349 1132 381 0", 
        "I 1136 347 1145 376 0", "F 1148 345 1171 375 0", "\u2018 1643 311 1784 314 0", ", 427 408 434 409 0", "a 1702 238 1743 255 0", 
        "V 49 396 52 398 0", ", 629 294 648 312 0", "0 1066 277 1090 314 0", "0 1101 270 1125 307 0", "0 1136 264 1162 301 0", 
        "0 1174 260 1199 296 0", "0 1211 255 1237 292 0", "0 1249 250 1275 287 0", "0 1288 244 1314 281 0", "0 1326 237 1353 275 0",
         "0 1368 232 1395 269 0", "0 1408 225 1435 263 0", "0 1448 219 1475 257 0", ". 1488 212 1516 251 0", ". 1529 205 1556 244 0", 
         ". 1570 199 1597 238 0", "l 1663 127 1670 280 0", "n 1679 192 1697 227 0", "- 1705 188 1738 201 0", "i 1756 130 1766 279 0", 
         "0 1813 162 1848 205 0", "0 1857 156 1891 198 0", "\u00a2 1902 150 1920 190 0"]}
    """

@APP.route('/ocr',  methods=['POST'])
def ocr():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        img = cv2.imdecode(numpy.fromstring(request.files['file'].read(), numpy.uint8), cv2.IMREAD_GRAYSCALE)
        img,_,_ = ir.resize_image(img)
        return ir.get_ocr_as_json(img)


@APP.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    # this is used for local testing only
    APP.run(host='127.0.0.1', port=8080, debug=True, threaded=False)
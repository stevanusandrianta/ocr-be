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
        img = cv2.imdecode(numpy.fromstring(request.files['file'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
        return ir.get_ocr_as_json(img)


@APP.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    # this is used for local testing only
    APP.run(host='127.0.0.1', port=8080, debug=True, threaded=False)
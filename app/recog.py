import os
import re
try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
import cv2
from imutils import contours
import json

class ImageRecognition():

    def __init__(self):
        self.max_height = 1024
        self.max_width = 1024


    def resize_image(self, img):
        max_height = self.max_height
        max_width = self.max_width
        h,w = img.shape
        # only shrink if img is bigger than required
        if max_height < h or max_width < w:
            # get scaling factor
            scaling_factor = max_height / float(h)
            if max_width/float(w) < scaling_factor:
                scaling_factor = max_width / float(w)
            # resize image
            img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
        
        h,w = img.shape
        return img,h,w

    #server
    def get_ocr_text(self, img):
        return pytesseract.image_to_string(img, config="--psm 6")


    def get_ocr_boxes(self, img):
        boxes = pytesseract.image_to_boxes(img, config="--psm 6") # also include any config options you use

        # draw the bounding boxes on the image
        for b in boxes.splitlines():
            b = b.split(' ')
            img = cv2.rectangle(img, 
                                (int(b[1]), h - int(b[2])), 
                                (int(b[3]), h - int(b[4])), 
                                (0, 255, 0),
                                2)
        return img


    def get_ocr_boxes_coordinate(self, img):
        boxes = pytesseract.image_to_boxes(img, config="--psm 6") # also include any config options you use
        return [b for b in boxes.splitlines()]


    def show_image(self, filename, img):
        cv2.imshow(filename, img)
        cv2.waitKey(1)
        cv2.destroyAllWindows()


    def extract_raw_ocr(self, text):
        res = re.findall(r'[\w\d]{2}[^\w\d\s]+[\w\d]{3}', text)
        res = res[0] if len(res)>0 else ''
        return re.sub('[^\w\d]', '-', res)
        
        
    def process(self, image_path):

        # read the image and get the dimensions
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img,h,w = self.resize_image(img)
        
        return get_ocr_text(img)

    def get_ocr_as_json(self, img):
        
        ocr_text = self.get_ocr_text(img)
        clean_ocr = self.extract_raw_ocr(ocr_text)
        ocr_box = self.get_ocr_boxes_coordinate(img)

        return(json.dumps(
            {
                'ocr' : ocr_text,
                'clean_ocr' : clean_ocr,
                'bounding_boxes' : ocr_box
            }
        ))
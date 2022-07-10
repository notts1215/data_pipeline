# -- coding: utf-8 --
"""
@Time : 2022/7/9 9:42
@Author : Zijie.XIANG
@Description : Obtain the info from images and output to a file.
"""
import base64
import glob
import hashlib
import os

import cv2
import json


def main():
    result_json = []
    pic_paths = glob.glob(
        os.path.join('./pipeline_data/images/image_data', '*.jpg'))  # This func returns a list with matched path inside. e.g. xxx.jpg

    # Using Haar
    classfier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    for pics in pic_paths[:1001]:
        image = cv2.imread(pics)
        file_name = os.path.split(pics)[-1].split('.')[0]
        md5 = hashlib.md5(open(pics, 'rb').read()).hexdigest()
        width = image.shape[1]
        height = image.shape[0]
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        # face detection and returns the face numbers
        face_no = len(classfier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=2, minSize=(5, 5)))
        result_json.append({
            'file_name': file_name,
            'md5': md5,
            'width': width,
            'height': height,
            'face_no': face_no
        })

    # writes into a file
    with open('./result.json', 'a', encoding='utf-8') as fw:
        for i in result_json:
            line = json.dumps(i, ensure_ascii=False)
            fw.write(line)
            fw.write("\n")
    print('finished')
    
    
if __name__ == '__main__':
    main()

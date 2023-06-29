# -*- coding: utf-8 -*-
import cv2
import base64

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]


image_L = cv2.imread('image/222.jpg')

image_L = cv2.resize(image_L, (320, 240), interpolation=cv2.INTER_LINEAR)


image_L_encode = cv2.imencode('.jpg', image_L, encode_param)[1]


image_L_base64 = base64.b64encode(image_L_encode)


image_L_data = image_L_base64.decode()

#测试更改

print()

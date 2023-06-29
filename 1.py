# -*- coding: utf-8 -*-

import shutil
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
import os
import cv2
import numpy as np
import warnings

warnings.filterwarnings("ignore")


def maskrcnn_init():
    global predictor_maskrcnn
    cfg_maskrcnn = get_cfg()
    cfg_maskrcnn.merge_from_file("./configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    cfg_maskrcnn.OUTPUT_DIR = './'
    cfg_maskrcnn.MODEL.WEIGHTS = os.path.join(cfg_maskrcnn.OUTPUT_DIR, 'model_0004799.pth')
    cfg_maskrcnn.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.98  # set the testing threshold for this model
    cfg_maskrcnn.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = (128)
    cfg_maskrcnn.MODEL.ROI_HEADS.NUM_CLASSES = 2
    cfg_maskrcnn.MODEL.DEVICE = 'cpu'
    predictor_maskrcnn = DefaultPredictor(cfg_maskrcnn)


maskrcnn_init()

path = r'F:\desktop\phoneshibie_image\phone_bmp'
seg_path = r'F:\desktop\phoneshibie_image\seg_image'

image_list = os.listdir(path)
for i in image_list:
    image_L = cv2.imread(os.path.join(path, str(i)))

    output = predictor_maskrcnn(image_L)
    num_yu = len(output['instances'].pred_boxes)
    if num_yu > 1:
        for j in range(num_yu):
            binary_img = output['instances'].pred_boxes.tensor[j].tolist()
            cropped_image = image_L[int(binary_img[1]):int(binary_img[1]) + int(binary_img[3] - binary_img[1]),
                            int(binary_img[0]):int(binary_img[0]) + int(binary_img[2] - binary_img[0]), :]
            tem_name = i.split('.')[0] + '_' + str(j) + '.bmp'
            cv2.imwrite(os.path.join(seg_path, tem_name), cropped_image)

        print(num_yu, end='\t')
        print(i)
    elif num_yu == 1:
        binary_img = output['instances'].pred_boxes.tensor[0].tolist()
        cropped_image = image_L[int(binary_img[1]):int(binary_img[1]) + int(binary_img[3] - binary_img[1]),
                        int(binary_img[0]):int(binary_img[0]) + int(binary_img[2] - binary_img[0]), :]
        cv2.imwrite(os.path.join(seg_path, i), cropped_image)
        print(i)
    else:
        cv2.imwrite(os.path.join(seg_path, str(i)), image_L)
        print('error', end='\t')
        print(i)

# 移动
# path = r'F:\desktop\shibie_image'
# for i in range(15):
#     path2 = os.path.join(path,str(i))
#     path3= os.path.join(path2,'adjust')
#     a = os.listdir(path3)
#     for num,j in enumerate(a):
#         shutil.move(os.path.join(path3,j), r'F:\desktop\shibie_image\all_image')


# # 重命名
# path = r'F:\desktop\shibie_image'
# for i in range(15):
#     path2 = os.path.join(path,str(i))
#     path3= os.path.join(path2,'adjust')
#     a = os.listdir(path3)
#     for num,j in enumerate(a):
#         new_name = (4 - len(str(i + 1))) * '0' + str(i + 1) + '_c1s'+ str(num+1)  + '.bmp'
#         os.rename(os.path.join(path3,j), os.path.join(path3,new_name))

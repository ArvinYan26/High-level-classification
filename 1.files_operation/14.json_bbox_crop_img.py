#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import json
import os
from PIL import Image
import cv2
import time
import matplotlib.pyplot as plt
def parse_json(label_path):
    """

    @param label_path: 标注的label信息，包括最小最大点和矩形框，box，调试的各个参数，ero，line_seg，line_leng，scale，label_type;标注的信息里面包括这些参数
    @return:
    """
    dict_info_list = []   # 存储所有信息，传进run的所有信息
    dict_info = dict()    # 存储图片信息
    print("label_path:", label_path, type(label_path))

    if label_path:

        _info = json.load(open(label_path, 'r', encoding='utf-8'))
        print("_info:", _info)
        shapes_info = _info['shapes']
    else:
        shapes_info = label_path
    print("_info['shapes']:", shapes_info)
    # 解析标注信息，将labelme中的shapes内容解析成列表
    for i, value in enumerate(shapes_info):
        if value['shape_type'] == 'rectangle':
            x_min, x_max = min(int(value['points'][0][0]), int(value['points'][1][0])), max(int(value['points'][0][0]),
                                                                                            int(value['points'][1][0]))
            y_min, y_max = min(int(value['points'][0][1]), int(value['points'][1][1])), max(int(value['points'][0][1]),
                                                                                           int(value['points'][1][1]))
            # box ：标注的小框，识别数字用的小框,存到字典里面用键值是：bbox
            if value['label'] == 'box':
                if 'num_point' not in dict_info.keys():
                    dict_info['num_point'] = [[x_min, y_min, x_max, y_max]]
                else:
                    dict_info['num_point'].append([x_min, y_min, x_max, y_max])
    return dict_info



def read_img_file(file_path, save_path):
    filelist = os.listdir(file_path)  # 文件夹下所有的子文件夹名（列表形式）
    count = 0
    # print("folderlist:", filelist)
    for file in filelist:
        # print("file:", file)
        if file.endswith(".json"):
            json_path = os.path.join(file_path, file)
            print("inner_path:", json_path)
            box_dict = parse_json(json_path)
            img_name = os.path.splitext(file)[0] + ".jpeg"
            img_path = os.path.join(file_path, img_name)
            img = cv2.imread(img_path)
            print(len(box_dict["num_point"]))
            for i, box in enumerate(box_dict["num_point"]):
                print("box:", i, box)
                crop_img = img[box[0]:box[2], box[1]:box[3]]
                # print(save_path + file)
                print("crop_img:", crop_img.shape)
                cv2.resizeWindow(20, 20)
                cv2.imshow("crop_img", crop_img)
                cv2.waitKey(1000)
                cv2.imwrite(str(i) + save_path + img_name, crop_img)




if __name__ == '__main__':
    path = "E:/Datasets/1.SubstationDatasets/AllSubstationsDatas/4.HuangBuSubstation/difficult_rec_img/num_data_9_10/"
    save_path = "E:/Datasets/1.SubstationDatasets/AllSubstationsDatas/4.HuangBuSubstation/difficult_rec_img/num_crop_img/"
    read_img_file(path, save_path)
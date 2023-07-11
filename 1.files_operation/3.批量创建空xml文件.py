#!/usr/bin/env python3
#功能：批量将图片 转单个xml 
import datetime
import json
import os
import io
import re
import fnmatch
import json
import numpy as np
import cv2 as cv 
from xml.dom.minidom import *

def generate_empty_xml(ROOT_DIR, img_path, save_ann_path):


    #图片输入路径
    IMAGE_DIR = os.path.join(ROOT_DIR, img_path)

    IMAGE_files=os.listdir(IMAGE_DIR)
    for annotation_filename in IMAGE_files:
        name1 = annotation_filename.split('.', 3)[0]
        mat_img = cv.imread(IMAGE_DIR+'/'+annotation_filename)
        [height,width,c]= mat_img.shape
        doc=Document()
        root=doc.createElement('annotation')
        doc.appendChild(root)
        #创建二级节点
        annotation=doc.createElement('size')
        name=doc.createElement('width')
        name.appendChild(doc.createTextNode(str(width))) #添加文本节点

        #创建一个带着文本节点的子节点
        ceo1=doc.createElement('height')
        ceo1.appendChild(doc.createTextNode(str(height)))
        ceo=doc.createElement('depth')
        ceo.appendChild(doc.createTextNode('3'))
        annotation.appendChild(name) #name加入到company
        annotation.appendChild(ceo1)
        annotation.appendChild(ceo)
        annotation1=doc.createElement('folder')
        annotation1.appendChild(doc.createTextNode('test_none'))
        annotation2=doc.createElement('filename')
        annotation2.appendChild(doc.createTextNode(annotation_filename))
        annotation3=doc.createElement('path')
        name9=IMAGE_DIR+'/'+annotation_filename
        annotation3.appendChild(doc.createTextNode(name9))
        annotation4=doc.createElement('source')
        name5=doc.createElement('database')
        name5.appendChild(doc.createTextNode('Unknown'))
        annotation4.appendChild(name5)

        annotation5=doc.createElement('segmented')
        annotation5.appendChild(doc.createTextNode('0'))
        root.appendChild(annotation)
        root.appendChild(annotation1)
        root.appendChild(annotation2)
        root.appendChild(annotation3)
        root.appendChild(annotation4)
        root.appendChild(annotation5)

        print(ceo.tagName)
        print(doc.toxml())
        #存成xml文件的位置
        filename1= save_ann_path + name1+'.xml'
        fp = open(filename1, 'w', encoding='utf-8')
        doc.writexml(fp, indent='', addindent='\t', newl='\n', encoding='utf-8')
        fp.close()

def generate_xml_pre(ROOT_DIR, img_path, save_ann_path):
    #图片输入路径
    IMAGE_DIR = os.path.join(ROOT_DIR, img_path)

    IMAGE_files=os.listdir(IMAGE_DIR)
    for annotation_filename in IMAGE_files:
        name1 = annotation_filename.split('.', 3)[0]
        mat_img = cv.imread(IMAGE_DIR + annotation_filename)
        [height, width, c]= mat_img.shape
        doc=Document()
        root=doc.createElement('annotation')
        doc.appendChild(root)


        annotation1=doc.createElement('folder')
        annotation1.appendChild(doc.createTextNode('test_none'))

        annotation2=doc.createElement('filename')
        annotation2.appendChild(doc.createTextNode(annotation_filename))

        annotation3=doc.createElement('path')
        name9=IMAGE_DIR+'/'+annotation_filename
        annotation3.appendChild(doc.createTextNode(name9))

        annotation4=doc.createElement('source')
        name5=doc.createElement('database')
        name5.appendChild(doc.createTextNode('Unknown'))
        annotation4.appendChild(name5)

        # 创建二级节点
        annotation = doc.createElement('size')
        name = doc.createElement('width')
        name.appendChild(doc.createTextNode(str(width)))  # 添加文本节点
        # 创建一个带着文本节点的子节点
        ceo1 = doc.createElement('height')
        ceo1.appendChild(doc.createTextNode(str(height)))
        ceo = doc.createElement('depth')
        ceo.appendChild(doc.createTextNode('3'))
        annotation.appendChild(name)  # name加入到company
        annotation.appendChild(ceo1)
        annotation.appendChild(ceo)

        annotation5=doc.createElement('segmented')
        annotation5.appendChild(doc.createTextNode('0'))

        #创建三级节点，循环添加
        annotation6=doc.createElement('object')
        name=doc.createElement('name')
        name.appendChild(doc.createTextNode("hand")) #添加类别名
        #创建一个带着文本节点的子节点
        ceo1=doc.createElement('pose')
        ceo1.appendChild(doc.createTextNode("Unspecified"))
        ceo2=doc.createElement('truncated')
        ceo2.appendChild(doc.createTextNode('0'))
        ceo3=doc.createElement('difficult')
        ceo3.appendChild(doc.createTextNode('0'))

        ceo4=doc.createElement('bandbox')
        xmin = 100
        ymin = 100
        xmax = 100
        ymax = 100

        c1 = ceo4.appendChild(doc.createElement("xmin"))
        c1.appendChild(doc.createTextNode(str(xmin)))
        c2 = ceo4.appendChild(doc.createElement("ymin"))
        c2.appendChild(doc.createTextNode(str(ymin)))
        c3 = ceo4.appendChild(doc.createElement("xmax"))
        c3.appendChild(doc.createTextNode(str(xmax)))
        c4 = ceo4.appendChild(doc.createElement("ymax"))
        c4.appendChild(doc.createTextNode(str(ymax)))
        ceo4.appendChild(c1)
        ceo4.appendChild(c2)
        ceo4.appendChild(c3)
        ceo4.appendChild(c4)


        annotation6.appendChild(name) #name加入到company
        annotation6.appendChild(ceo1)
        annotation6.appendChild(ceo2)
        annotation6.appendChild(ceo3)
        annotation6.appendChild(ceo4)

        #将节点信息添加到roo下

        root.appendChild(annotation1)
        root.appendChild(annotation2)
        root.appendChild(annotation3)
        root.appendChild(annotation4)
        root.appendChild(annotation)
        root.appendChild(annotation5)
        root.appendChild(annotation6)

        print(ceo.tagName)
        print(doc.toxml())
        #存成xml文件的位置
        filename1= save_ann_path + name1+'.xml'
        fp = open(filename1, 'w', encoding='utf-8')
        doc.writexml(fp, indent='', addindent='\t', newl='\n', encoding='utf-8')
        fp.close()


def change_content_xml(path):
    """
    :param path:原xml文件位置
    :return:
    """
    files = os.listdir(path)  # 返回文件夹中的文件名列表
    for xmlFile in files:

        if not os.path.isdir(xmlFile):  # os.path.isdir()用于判断对象是否为一个目录
            # 如果不是目录，则直接打开
            # name1 = xmlFile.split('.')[0]
            name1 = "hand"
            # print(name1)
            dom = xml.dom.minidom.parse(path + xmlFile)
            # print(dom)
            root = dom.documentElement
            newfolder = root.getElementsByTagName('folder')
            # print(newfolder)
            newpath = root.getElementsByTagName('path')
            # newfilename = root.getElementsByTagName('filename')
            # newfilename[0].firstChild.data = name1

            newfilename = root.getElementsByTagName('name')  # 含有name的标题的列表。

            # print("newfilename:", newfilename)

            for i in range(len(newfilename)):
                count = 0
                if newfilename[i].firstChild.data != "hand":
                    newfilename[i].firstChild.data = name1  # 修改标注目标的类别名
                    # count += 1
                # print("修改次数:", count)
            with open(os.path.join(path, xmlFile), 'w') as fh:
                dom.writexml(fh)
    print('写入name/pose OK!')
    # print("总数:", count)

if __name__ == '__main__':

    ROOT_DIR = "E:/PycharmProjects/2.ObjectDetections/0.1.files_operation"
    img_path = "E:/datasets/4.hand_keypoints/extra/negivate/"
    save_ann_path = "E:/datasets/4.hand_keypoints/extra/test/"
    #generate_empty_xml(ROOT_DIR, img_path, save_ann_path)


    #修改xml中特定的内容
    #path = "E:/datasets/gesture_keypoints_videos/new_dataset/hand_datasets(all)/Validation_data/Annotations/"
    #change_content_xml(path)

    #将预测信息携程xml文件
    generate_xml_pre(ROOT_DIR, img_path, save_ann_path)
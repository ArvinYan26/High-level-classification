'''
Author: your name
Date: 2021-09-07 17:06:55
LastEditTime: 2021-10-19 15:12:54
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \2.ObjectDetections\0.1.files_operation\9.change_content_xml.py
'''
# -*- coding: utf-8 -*-
import os
import os.path
import xml.dom.minidom


def check_img_xml(path, name1):
    files = os.listdir(path)#返回文件夹中的文件名列表
    #print(files)
    s=[]

    count = 0
    for xmlFile in files:
        count += 1
        if not os.path.isdir(xmlFile):#os.path.isdir()用于判断对象是否为一个目录
            #如果不是目录，则直接打开
            #name1 = xmlFile.split('.')[0]
            #print(name1)
            print("文件：", xmlFile)
            dom = xml.dom.minidom.parse(path + xmlFile)
            #print(dom)
            root = dom.documentElement
            newfolder = root.getElementsByTagName('folder')
            #print(newfolder)
            newpath = root.getElementsByTagName('path')
            #newfilename = root.getElementsByTagName('filename')
            #newfilename[0].firstChild.data = name1

            newfilename = root.getElementsByTagName('name') #含有name的标题的列表。

            #print("newfilename:", newfilename)
            if len(newfilename) > 0:
                for i in range(len(newfilename)):
                    count = 0
                    if newfilename[i].firstChild.data != name1:
                        newfilename[i].firstChild.data = name1       #修改标注目标的类别名
                        #count += 1
                    #print("修改次数:", count)
                with open(os.path.join(path, xmlFile), 'w') as fh:
                    dom.writexml(fh)
                    #print('写入name/pose OK!')
    count += 1

    print("总数:", count)

if __name__ == "__main__":

    path = path = "E:/datasets/3.1hand_gesture/v5-9/slected_TFS/selected2/three/final/Annotations/"
    name1 = "three"
    check_img_xml(path, name1)
    



'''
Author: your name
Date: 2021-09-07 17:06:55
LastEditTime: 2021-10-21 17:59:25
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \PycharmProjects\2.ObjectDetections\1.files_operation\2.随机划分数据集.py
'''
import os
import random
import shutil


def get_imlist(path):
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]

def get_xmllist(path):
    return [os.path.join(path, l) for l in os.listdir(path) if l.endswith('.xml')]



def getData(src_path, src_xml, test_img, test_xml, p):
    """

    :param src_path: all the images
    :param src_xml: all the annotations
    :param test_img: test data
    :param test_xml: test annotations
    :param p: percentage of dataset split(division)
    :return:
    """
    xmllist = []
    #创建测试集数据集
    img_list = get_imlist(src_path)
    print("img_list:", len(img_list))
    random.shuffle(img_list)
    le = int(len(img_list) * p)  # 这个可以修改划分比例
    for f in img_list[le:]:
        shutil.move(f, test_img)

        print("f:", f)
        #将对应的xml文件移走
    for i in os.listdir(test_img):  #os.listdir：读取图片名称
        xmllist.append(os.path.splitext(i)[0] + '.xml')  #add the suffix(后缀) of the xml file

    print("xmlfilepath:", xmllist)

    for i in xmllist:
        #xmlfilepath = os.path.join(src_xml, i)  #将挑选的数据存入列表
        #print("xmlfilepath:", xmlfilepath)
        or_xml = src_xml + '/' + i
        print("or_xml:", or_xml)
        #print(xmlfilepath)
        shutil.move(or_xml, test_xml)
    print("test_xml:", os.listdir(test_xml))

def image_split(src_path, test_img, p):
    """
    :param src_path: all the images
    :param src_xml: all the annotations
    :param test_img: test data
    :param test_xml: test annotations
    :param p: percentage of dataset split(division)
    :return:
    """
    #创建测试集数据集
    img_list = get_imlist(src_path)
    print("img_list:", len(img_list))
    random.shuffle(img_list)
    le = int(len(img_list) * p)  # 这个可以修改划分比例
    for f in img_list[le:]:
        shutil.move(f, test_img)

        print("f:", f)


if __name__ == '__main__':
    #原数据集路径
    src_img_path = 'E:/Datasets/biandianzhan1/train/images'
    src_xml_path = 'E:/Datasets/biandianzhan1/train/annotations'

    #划分的新的测试集的路径,这几个需要提前创建好
    test_img = "E:/Datasets/biandianzhan1/test/images"
    test_xml = "E:/Datasets/biandianzhan1/test/annotations"
    #p：划分比例
    # 划分数据集图像与xml
    # getData(src_img_path, src_xml_path, test_img, test_xml, p=0.8)

    # 只划分图像
    image_split(src_img_path, test_img, p=0.8)


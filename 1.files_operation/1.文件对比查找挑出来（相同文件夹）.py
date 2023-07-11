# -*- coding: utf-8 -*-
import os
import shutil
import cv2 as cv
from xml.dom.minidom import *

#path1 = r'../diff'

def file_name(path1):

    """
    图片和xml文件在同一个文件夹下，相同文件夹下的
    :param file_dir:文件夹位置
    :return:
    """
    jpg_list = []
    xml_list = []

    #相同文件夹内的图片和xml文件区别开来，分别存放
    for root, dirs, files in os.walk(path1):
        for file in files:
            # 其中os.path.splitext()函数将路径拆分为文件名+扩展名
            if os.path.splitext(file)[1] == '.jpg':
                jpg_list.append(os.path.splitext(file)[0])
            elif os.path.splitext(file)[1] == '.xml':
                xml_list.append(os.path.splitext(file)[0])

    diff = set(xml_list).difference(set(jpg_list))  # 差集，在a中但不在b中的元素
    print(len(diff))
    for name in diff:
        #print("no jpg", name + ".xml")
        os.remove(path1 + "Annotations/" + name + ".xml")
        print("after_no jpg", name + ".xml")
        
    diff2 = set(jpg_list).difference(set(xml_list))  # 差集，在b中但不在a中的元素

    for name in diff2:
        #print("no xml", name + ".jpg")
        os.remove(path1 + "JPEGImages/" + name + ".jpg")
        print("after_no xml", name + ".jpg")
    print(len(diff2))

    return diff2

def select_no_ann_img(img_name, path2, path3):

    for name in img_name:

        print(name)
        shutil.move(path2+'\\'+name+'.jpg', path3)
        print("no xml", name + ".jpg")


def remove_different_img(file1_path, file2_path):

    list1 = os.listdir(file1_path)
    file_list1 = []  # annotations中的文件名列表 不带后缀
    for i in list1:
        file_list1.append(os.path.splitext(i)[0])
    # print(file_list1)

    list2 = os.listdir(file2_path)
    file_list2 = []  # image中的文件名列表 不带后缀

    for i in list2:
        file_list2.append(os.path.splitext(i)[0])
    # print(file_list2)
    # 找出没有标注的图片名称列表
    b = [y for y in file_list1 if y not in file_list2]
    # 把这些列表加上扩展名 然后将其删除
    #path = r'F:\目标检测\数据标注\test\image_f'
    print("b:", len(b))
    for i in b:
        #os.remove(os.path.join(path, i + '.jpg'))
        #os.remove(file1_path + '/' + i + '.jpg')
        new_path = "E:/datasets/gesture_keypoints_videos/new_dataset/1"
        shutil.copy(file1_path + '/' + i + '.jpg', new_path)

def remove_jpg(file_path, new_path, img_format):
    #删除图像，或者移走图像
    list1 = os.listdir(file_path)
    count = 0
    for file in list1:
        if os.path.splitext(file)[1] == img_format:
            #os.remove(file_path + file)
            #shutil.move(file_path + file, new_path)
            os.remove(file_path + file)
            count += 1
    print("删除完毕！", count)

if __name__ == '__main__':

    #需要对比的原文件路径（里面包含图像和xml两个文件夹）
    path1 = 'E:/datasets/3.1hand_gesture/v5-11/Validation_data/'
    
    #path1 = 'E:/datasets/gesture_keypoints_videos/new_dataset/hand_datasets(all)/all/chnagebf'
    file_name(path1)

    #总图像数据集文件路径（路径文件夹下只有图像）
    #path2 = r'C:\Users\Yan\Desktop\qinxu1\JPEGImages'
    #存放未标注的图像文件夹
    #path3 = r'C:\Users\Yan\Desktop\empty'
    #no_ann_name = file_name(path1)
    #print(no_ann_name)
    #select_no_ann_img(no_ann_name, path2, path3)

    #path3 = r'C:\Users\Yan\Desktop\test_none'
    #将未标记的图像生成xml文件路径
    #path4 = r"C:\Users\Yan\Desktop\ann"
    #generate_empty_xml(path3, path4)


    """
    #删除原文件夹下与新文件夹下不同的文件
    file1_path = 'E:/datasets/gesture_keypoints_videos/new_dataset/JPEGImages_all' #原图像文件夹
    file2_path = 'E:/datasets/gesture_keypoints_videos/new_dataset/test_img'  #标注过的图像文件夹
    remove_different_img(file1_path, file2_path)
    """

    #移除jpg文件
    # file_path = "E:/datasets/6.smoking_calling/smoking/smoking2/"
    # img_format = ".gif"
    # new_path = "E:/datasets/3.1hand_gesture/ges/JPEGImags/"
    # remove_jpg(file_path, new_path, img_format)
    #
    # print("done")

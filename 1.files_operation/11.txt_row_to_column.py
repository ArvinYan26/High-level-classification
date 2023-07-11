'''
Author: your name
Date: 2021-09-07 17:06:55
LastEditTime: 2021-11-09 16:17:53
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \PycharmProjects\2.ObjectDetections\1.files_operation\11.txt_row_to_column.py
'''
import os
import cv2


def delet_empty_row(txt_file, column_txt):
    fw = open(column_txt, 'w')
    with open(txt_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().replace("\n", '')  # strip去掉两边空格，用\n代替空格
            if len(line) != 0:
                #print(line)
                fw.write(line)
                fw.write('\n')


def row_to_column(save_txt_path, column_txt, img_path):
    """
    将横行的txt文件转化为竖行
    :param save_txt_path:
    :param column_txt:
    :param img_path:
    :return:
    """
    files = os.listdir(img_path)
    count = 0
    with open(column_txt, "r") as f:
        data = f.readlines()
        for line in data:
            count += 1
            s = (line.strip('\n').split(','))[0].split()
            new_s = s[:42]   #取出来关键点坐标
            name = s[-1:]    #取出来图像名字
            #print(len(new_s))
            #print(new_s, name)
            new_file_name = name[0].split(".")[0] + ".txt"

            #找到对应的图像文件获取图像高宽，归一化用
            img_file = img_path + name[0]    #(找到文件图片)
            img = cv2.imread(img_file)
            h, w, c = img.shape
            #print("高，宽：", h, w)
            f = open(save_txt_path + new_file_name, "w")    
            f.write(str(21))   #首行关键点个数写入
            f.write("\n")
            l = int(len(new_s)/2)
            #print(l)
            for i in range(0, l):
                #print(i, new_s[(i*2):(i*2+2)])
                one_key_cor = list(map(float, new_s[(i*2):(i*2+2)]))
                #print("归一化前的坐标：", one_key_cor)
                one_key_cor = [round(one_key_cor[0]/w, 3), round(one_key_cor[1]/h, 3)]
                #print("归一化后的坐标：", one_key_cor)
                one_key_cor = map(str, one_key_cor)
                point1 = " ".join((one_key_cor))   #去掉字符串中的空格
                print(type(point1), point1)
                f.write(str(point1))
                f.write("\n")

def get_name_vector(name_txt):
    base_data = []
    with open(name_txt, "r") as f:
        data = f.readlines()

        for line in data:
            # 直接去掉每一行的开头结尾的换行符，按“，”分隔元素，行成列表
            line = list(line.strip('\n').split(','))  
            # 将列表中第一个元素用空格分隔开， 第一个是名字，第二个是特征值
            elem_0 = line[0].split(" ")
            name = elem_0[0]    #名字
            line.insert(1, elem_0[1])   #将原始数据的第一个元素也添加进后边，形成完整的不含名字的128维向量
            vector1 = list(map(float, line[1:]))   #将字符串的向量转化为浮点型
            vector1.insert(0, name)  #append函数没有返回值，不要去接受返回， 将名字添加进列表开头
            base_data.append(vector1)  #将每一个人的名字向量添加进列表形成数据库
            print(len(base_data), len(base_data[0]), base_data)
    return base_data

if __name__ == '__main__':
    # #将txt文件中的行文件转化成列
    # or_kepoints_txt = "E:/PycharmProjects/2.ObjectDetections/0.1.files_operation/data/"
    # txt_file = or_kepoints_txt + "labels.txt"
    # column_txt = or_kepoints_txt + "label.txt"
    # #delet_empty_row(txt_file, column_txt)

    # save_txt = "E:/PycharmProjects/2.ObjectDetections/0.1.files_operation/data/labels/"
    # img_path = "E:/PycharmProjects/2.ObjectDetections/0.1.files_operation/data/JPEGImages/"
    # row_to_column(save_txt, column_txt, img_path)

    # #得到txt文件中的每行数据的名字和向量,存储成列表或者字典
    txt_file = "C:/Users/15638/Desktop/img_v3/" + "name_vector.txt"
    get_name_vector(txt_file)









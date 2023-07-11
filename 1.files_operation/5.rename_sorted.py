# -*- coding:utf8 -*-
import os
import shutil

import cv2


def rename(or_path, new_path):
    #filelist = os.listdir(self.or_path)  # 获取文件路径
    folderlist = os.listdir(or_path)  # 文件夹下所有的子文件夹名（列表形式）
    print("folderlist:", folderlist)  #

    for folder in folderlist:
        inner_path = os.path.join(or_path, folder)
        total_num_folder = len(folderlist)  # 文件夹下的子文件夹的总数
        #print('total have %d folders' % (total_num_folder))  # 打印文件夹的总数


        filelist = os.listdir(inner_path)  # 列举图片
        #print(filelist)

        i = 0
        for j, item in enumerate(filelist):
            total_num_file = len(filelist)  # 单个文件夹内图片的总数
            print("j, num:", (j, total_num_file))
            if item.endswith('.png'):
                src_name = os.path.join(os.path.abspath(inner_path), item)  # 原图的地址
                new_name = os.path.join(os.path.abspath(inner_path), str(folder) + '_' + str(
                    i) + '.png')  # 新图的地址（这里可以把str(folder) + '_' + str(i) + '.jpg'改成你想改的名称）
                try:
                    os.rename(src_name, new_name)
                    """
                    copy重命名后的图像到新的文件夹下
                    """
                    shutil.copy(new_name, new_path)  #将新图片copy一份到新的文件夹
                    print('converting %s to %s ...' % (src_name, new_name))

                    i += 1
                except:
                    continue

# def copy_img_mutil(or_path, new_img_path, new_xml_path):
def copy_img_mutil(or_path, new_img_path):
    """
    文件夹下多个子文件夹下的所有图片
    :param or_path:源文件夹
    :param new_path: 新文件夹
    :return:
    """


    for root, dirs, files in os.walk(or_path):

        print("root:", root)
        print("dirs:", dirs)
        print("files:", files)

        # if len(files) == 2:
        for id, item in enumerate(files):
            #total_num_file = len(filelist)  # 单个文件夹内图片的总数
            #print("j, num:", (j, total_num_file))
            # print("item:", item)    #名字
            # if id == 1 and item.endswith('.jpg'):
            if item.endswith('.jpg'):
                # id==1:将文件夹下的第二张图像copy出来到新的文件夹
                img_path = root + '/' + item
                root_0, name = os.path.split(root)
                if not name == "label":
                    # print("root_0, name:", root_0, name)
                    folder = os.path.exists(new_img_path)
                    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
                        os.makedirs(new_img_path)
                    new_path1 = new_img_path + item  # 将命名后的新文件copy到新的文件夹下， '/'：路径的意思
                    shutil.copy(img_path, new_path1)  # 将新图片copy一份到新的文件夹

        # if len(files) == 1:
        #     if files[0].endswith('.jpg'):
        #         # id==1:将文件夹下的第二张图像copy出来到新的文件夹
        #         img_path = root + '/' + files[0]
        #         root_0, name = os.path.split(root)
        #         if not name == "label":
        #             # print("root_0, name:", root_0, name)
        #             new_path1 = new_img_path + files[0]  # 将命名后的新文件copy到新的文件夹下， '/'：路径的意思
        #             shutil.copy(img_path, new_path1)  # 将新图片copy一份到新的文件夹
        #     # #将对应的xml文件也移到新的文件夹下
        #     # elif item.endswith('.xml'):
        #     #     xml_path = root + '/' + item
        #     #
        #     #     new_path2 = new_xml_path  + item  # 将命名后的新文件copy到新的文件夹下， '/'：路径的意思
        #     #
        #     #     shutil.copy(xml_path, new_path2)  # 将新图片copy一份到新的文件夹

    print("done")

def copy_xml(or_path, new_path):
    """
    将原文件夹下多个文件夹下的子文件拷贝到新的同一个文件夹下
    """
    folderlist = os.listdir(or_path)  # 文件夹下所有的子文件夹名（列表形式）
    #print("folderlist:", folderlist)  #

    count = 0
    for folder in folderlist:
        inner_path = os.path.join(or_path, folder)
        filelist = os.listdir(inner_path)  # 列举文件
        sub_count = 0
        for j, item in enumerate(filelist):
            #total_num_file = len(filelist)  # 单个文件夹内图片的总数
            #print("j, num:", (j, total_num_file))

            if item.endswith('.jpg'):
                item = or_path + '/' + folder + '/' + item
                #name = str(j) + '.jpg'
                #new_item = or_path + '/' +   # 将命名后的新文件copy到新的文件夹下， '/'：路径的意思
                shutil.copy(item, new_path)

  # 将新图片copy一份到新的文件夹
                count += 1
        sub_count += 1
        print("sub_img_img:", sub_count)

    print("all_img_num:", count)



def copy_img_single(or_path, new_path):
    """
     删除单个文件夹下的特定尺寸的图像
    :param or_path:源文件夹
    :param new_path: 新文件夹
    :return:
    """
    folderlist = os.listdir(or_path)  # 文件夹下所有的子文件夹名（列表形式）
    # print("folderlist:", folderlist)  #

    count = 0
    for i, name in enumerate(folderlist):
        # i += 1654
        #inner_path = os.path.join(or_path, folder)
        #filelist = os.listdir(inner_path)  # 列举图片
        #for j, item in enumerate(filelist):

        if name.endswith('.jpeg'):
            img = cv2.imread(or_path + name)
            print(img.shape[0])
            if img.shape[0] < 800:
                print(img.shape[0])   #图像高度
                # shutil.move(name, new_path)  # 将新图片copy一份到新的文件夹
                print(or_path + name)
                os.remove(or_path + name)
                count += 1

    print("num_img:", count)

def img_rename(img_path, letter, xml_path, count):
    files = os.listdir(img_path)
    for i, file in enumerate(files):
        count += 1
        name =os.path.splitext(file)[0]  #将文件名分割成  名字 + 扩展名
        file = img_path + file
        new_img_name = img_path + letter + str(count) + '.jpg'  # 将命名后的新文件copy到新的文件夹下， '/'：路径的意思
        #将xml文件也重命名
        # if os.path.exists("1-" + str(count) + ".jpg"): #哦按段是否存在 

        xml_file = xml_path + name + ".xml"

        new_xml_name = xml_path + letter + str(count) + '.xml'  # 将命名后的新文件copy到新的文件夹下， '/'：路径的意思
        
        os.rename(file, new_img_name)
        os.rename(xml_file, new_xml_name)
        
        
        #shutil.move(new_name, new_path)  # 将新图片copy一份到新的文件夹
    
    print("done")


def rename_img_xml(img_path, xml_path, prefix):
    #将特定字符命名的图片重命名，同事对应的xml文件重命名
    files = os.listdir(img_path)
    count = 488
    for i, file in enumerate(files):
        print("file0:", file)
        if file[:len(prefix)] == prefix:
            print("file1:", file)
            count += 1
            name =os.path.splitext(file)[0]  #将文件名分割成  名字 + 扩展名
            #if os.path.exists("1-" + str(count) + ".jpg"): #按段是否存在
            file = img_path + file
            print("name:", name)
            new_img_name = img_path + "013-" + str(count) + '.jpg'  # 将命名后的新文件copy到新的文件夹下， '/'：路径的意思
            xml_file =  xml_path + name + ".xml"
            new_xml_name = xml_path + "013-" + str(count) + ".xml"
            # print(new_name)
            # print(new_name, new_path)
            os.rename(xml_file, new_xml_name)
            os.rename(file, new_img_name)
            
            #shutil.move(new_name, new_path)  # 将新图片copy一份到新的文件夹

def copy_prefix_img_xml(img_path, xml_path, new_img_path, new_xml_path, prefix):
    #复制特定前缀的图及xml到其他文件夹
    files = os.listdir(img_path)
    count = 0
    for i, file in enumerate(files):
        print("file0:", file)
        if file[:len(prefix)] == prefix:
            print("file1:", file)
            
            name =os.path.splitext(file)[0]  #将文件名分割成  名字 + 扩展名
            #if os.path.exists("1-" + str(count) + ".jpg"): #哦按段是否存在
            file = img_path + file
            print("name:", name)
            xml_file =  xml_path + name + ".xml"
            # shutil.copy(file, new_img_path)
            # shutil.copy(xml_file, new_xml_path)
            shutil.move(file, new_img_path)
            shutil.move(xml_file, new_xml_path)
            count += 1
    print("count:", count)

def delete_prefix_img_xml(img_path, xml_path, prefix):
     #复制特定前缀的图及xml到其他文件夹
    files = os.listdir(img_path)
    count = 0
    for i, file in enumerate(files):
        print("file0:", file)
        if file[:len(prefix)] == prefix:
            print("file1:", file)
            
            name =os.path.splitext(file)[0]  #将文件名分割成  名字 + 扩展名
            #if os.path.exists("1-" + str(count) + ".jpg"): #哦按段是否存在
            file = img_path + file
            print("name:", name)
            xml_file =  xml_path + name + ".xml"
            os.remove(file)
            os.remove(xml_file)
            count += 1
    
    print("count:", count)

def resize_img(img_path, new_size):
    # files = os.listdir(img_path)
    # for file in files:
    #     print("file:", file)
    #     img = cv2.imread(img_path + file, cv2.IMREAD_GRAYSCALE)  # 读取为灰度图,
    #     img = cv2.resize(img, new_size, interpolation=cv2.INTER_CUBIC)
    #     cv2.imwrite(img_path + file, img)
    print(img_path)
    img = cv2.imread(img_path)  # 读取为灰度图,
    print("img:", img)
    img = cv2.resize(img, new_size, interpolation=cv2.INTER_CUBIC)
    cv2.imwrite("D:/DesktopWallpaper/Ghost_Blade/new_4k.png", img)



if __name__ == '__main__':
    #1.重命名文件下所有子文件夹夹下所有图片名称
    # letter = "m"
    or_path = 'E:/CompanyDocuments/PonyRobot/6.SubstationProjects/4.SubstationDatasets/4.HuangBu/181out_door/device_picture/'  # 表示需要命名处理的文件夹
    
    new_img_path = 'E:/CompanyDocuments/PonyRobot/3.LearningFiles/项目学习/2.变电站识别结果/黄埠变电站/167保护室/20220816/JPEGImages/'   #创建的新文件夹
    # new_xml_path = "E:/datasets/1/train_data/Annotations/"
    # copy_img_mutil(or_path, new_img_path, new_xml_path)
    # copy_img_mutil(or_path, new_img_path)
    copy_img_single(or_path, new_img_path)

    #rename(or_path, new_path)

    #2.重命名的那个文件夹下的所有图片名称
    #str_name = str(12)
    #copy_img_single(or_path, new_path)
    #copy_img_mutil(or_path, new_path)
    #new_path = r'C:\Users\Yan\Desktop\new_name_img\five'
    #move_img(new_path)

    # 3.仅重命名
    # img_path = "D:/datasets/Safety_Helmet/Hard_Hat/images/"
    # xml_path = "D:/datasets/Safety_Helmet/Hard_Hat/Annotations/"
    # letter = "00"
    # img_rename(img_path, letter, xml_path, count=0)


    # #4.将文件夹下多个子文件移到同一个新的文件夹下
    # or_path = "E:/datasets/datasets/final_datasets/arvin/imgs"
    # new_path = "E:/datasets/datasets/final_datasets/arvin/JPEGImages"
    # copy_xml(or_path, new_path)

    #4.重命名特定前缀的图像的名字和对应的xml文件
    # img_path = 'E:/datasets/1/train_data/JPEGImages/'  # 表示需要命名处理的文件夹
    # xml_path = 'E:/datasets/1/train_data/Annotations/'
    # prefix = "01-"
    # rename_img_xml(img_path, xml_path, prefix)

    # #5.复制特定前缀的图及xml到其他文件夹
    # img_path = 'E:/datasets/3.1hand_gesture/v5-11/v5-10/train_data/JPEGImages/'  # 表示需要命名处理的文件夹
    # xml_path = 'E:/datasets/3.1hand_gesture/v5-11/v5-10/train_data/Annotations/'
    # new_img_path = "E:/datasets/3.1hand_gesture/v5-11/v5-9/348/JPEGImages/"
    # new_xml_path = "E:/datasets/3.1hand_gesture/v5-11/v5-9/348/Annotations/"
    # prefix = "13-"
    # copy_prefix_img_xml(img_path, xml_path, new_img_path, new_xml_path, prefix)

    # 6.删除特定前缀的图像和xml文件
    # img_path = 'E:/datasets/3.1hand_gesture/v5-9/v5-9/train_data/JPEGImages/'  # 表示需要命名处理的文件夹
    # xml_path = 'E:/datasets/3.1hand_gesture/v5-9/v5-9/train_data/Annotations/'
    # prefix = "8-"
    # delete_prefix_img_xml(img_path, xml_path, prefix)

    # 7.resize img
    # img_path = "D:/DesktopWallpaper/Ghost_Blade/4k.png"
    # new_size = (2560, 1600)
    # resize_img(img_path, new_size)
    #

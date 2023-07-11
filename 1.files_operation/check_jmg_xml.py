
import os
import cv2
import numpy as np


def check_images(file_dir):
    '''
    目录结构：
    dataset/
        jpegs/
        xmls/
    :param file_dir:
    :return:
    '''

    jpg_list = []
    xml_list = []

    not_img_list = []

    for root, dirs, files in os.walk(file_dir):
        print('root, dirs,', root, dirs)
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                jpg_list.append(os.path.splitext(file)[0])

                # 图片读入检查
                img = cv2.imread(os.path.join(root, file), cv2.IMREAD_COLOR)

                if not isinstance(img, np.ndarray):
                    not_img_list.append(os.path.splitext(file)[0])

            elif os.path.splitext(file)[1] == '.xml':
                xml_list.append(os.path.splitext(file)[0])


    print("标签文件总数：", len(xml_list))
    print("图片文件总数：", len(jpg_list))

    print("不能正常读取的图片总数：", len(not_img_list))
    print("不能正常读取的图片列表：", str(not_img_list))

    diff = set(xml_list).difference(set(jpg_list))  # 差集，在a中但不在b中的元素
    for name in diff:
        print("no jpg", name + ".xml")

    diff2 = set(jpg_list).difference(set(xml_list))  # 差集，在b中但不在a中的元素
    for name in diff2:
        print("no xml", name + ".jpg")


if __name__ == '__main__':

    path = '/Users/liqing/Desktop/images'
    check_images(path)


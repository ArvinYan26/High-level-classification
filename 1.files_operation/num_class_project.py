import os
import os.path
import xml.dom.minidom
from collections import Counter
import xml.etree.ElementTree as ET


def check_img_xml(path, replace_dict):
    """
    修改xml里面标记错的类别名
    """
    files = os.listdir(path)#返回文件夹中的文件名列表
    # print(files)
    s = []
    count = 0
    for xmlFile in files:
        # count += 1
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

            print("newfilename:", type(newfilename), len(newfilename))
            # count = 0
            if len(newfilename) > 0:
                for i in range(len(newfilename)):
                    print(i, newfilename[i].firstChild.data)


                    # correct_name = newfilename[i].firstChild.data
                    if newfilename[i].firstChild.data in replace_dict:
                        newfilename[i].firstChild.data = replace_dict[newfilename[i].firstChild.data]       #修改标注目标的类别名
                    print(i, newfilename[i].firstChild.data)
                with open(os.path.join(path, xmlFile), 'w') as fh:
                    dom.writexml(fh)
                    #print('写入name/pose OK!')

    print("总数:", count)

def count_img_opj(path, calsses, class_img, pro_num):
    """
     统计每个类别图像个数，及类别目标个数 xml.dom方式
     """
    files = os.listdir(path)  # 返回文件夹中的文件名列表
    # print(files)
    s = []
    count = 0
    for xmlFile in files:
        # count += 1
        if not os.path.isdir(xmlFile):  # os.path.isdir()用于判断对象是否为一个目录
            # 如果不是目录，则直接打开
            # name1 = xmlFile.split('.')[0]
            # print(name1)
            # print("文件：", xmlFile)
            dom = xml.dom.minidom.parse(path + xmlFile)
            # print(dom)
            root = dom.documentElement
            newfolder = root.getElementsByTagName('folder')
            # print(newfolder)
            newpath = root.getElementsByTagName('path')
            # newfilename = root.getElementsByTagName('filename')
            # newfilename[0].firstChild.data = name1

            name = []
            newfilename = root.getElementsByTagName('name')  # 含有name的标题的列表。

            # print("newfilename:", type(newfilename), len(newfilename))
            # count = 0
            if len(newfilename) > 0:
                for i in range(len(newfilename)):
                    # print(i, newfilename[i].firstChild.data)
                    name.append(newfilename[i].firstChild.data)

            cal_img = Counter(list(set(name)))
            result = Counter(name)
            for key_name in cal_img.keys():
                if key_name in calsses:
                    class_img[key_name] += cal_img[key_name]
                    pro_num[key_name] += result[key_name]

    print("class_img:", class_img)
    print("pro_num:", pro_num)

    # print("总数:", count)

def count_img_opj_tree(path, calsses, class_img, pro_num):
    """
     统计每个类别图像个数，及类别目标个数，ET.parse方式
     """
    files = os.listdir(path)  # 返回文件夹中的文件名列表
    # print(files)
    s = []
    count = 0
    for xmlFile in files:
        # count += 1
        if not os.path.isdir(xmlFile):  # os.path.isdir()用于判断对象是否为一个目录
            # 如果不是目录，则直接打开
            # name1 = xmlFile.split('.')[0]
            # print(name1)
            # print("文件：", xmlFile)
            file = open(path+xmlFile, "rb")
            root = ET.parse(file)
            # root = ET.parse(path + xmlFile)

            name = []
            # newfilename = root.getElementsByTagName('name')  # 含有name的标题的列表。
            newfilename = root.findall("object")
            print("newfilename:", newfilename)
            for sub_obj in newfilename:
                obj_name = sub_obj.find("name").text
                name.append(obj_name)

            cal_img = Counter(list(set(name)))
            result = Counter(name)
            for key_name in cal_img.keys():
                if key_name in calsses:
                    class_img[key_name] += cal_img[key_name]
                    pro_num[key_name] += result[key_name]

    print("class_img:", class_img)
    print("pro_num:", pro_num)

def dict_add(calss_list, obj_num_list):
    # A = {'a': 1, 'b': 2, 'c': 3}
    # B = {'b': 4, 'c': 6, 'd': 8}
    # li = []
    # li.extend((cla_img2, cla_img3, cla_img4, cla_img5, cla_img6))
    # print(len(li))
    for i in range(len(class_list)):
        print(i)
        for key, value in calss_list[i].items():
            if key in calss_list[0]:
                calss_list[0][key] += value

    for i in range(len(obj_num_list)):
        print(i)
        for key, value in obj_num_list[i].items():
            if key in obj_num_list[0]:
                obj_num_list[0][key] += value

    print("add_result:", calss_list[0], obj_num_list[0])


if __name__ == "__main__":
    # 类别名
    # classes = ['wcgz', 'xy', 'wdaqm', 'bpmh', 'bpps', 'gbps', 'nc', 'gkxfw', 'xmbhyc', 'dmyw', 'gjbs', 'gjtps',
    #            'hxqyfywyc', 'wkps', 'dsyc', 'helmet', 'jyzps', 'bjzc']
    # # 关键字是错误的名字，元素是正确的名字
    # replace_dict = {'jytpl': 'jyzps', 'bjps': 'bpps', 'hxjyfywyc': 'hxqyfywyc', 'bjduyc': 'dsyc', 'bjmh': 'bpmh',
    #                 'bpdsyc': 'dsyc',
    #                 'gkxw': 'gkxfw', 'smbhyc': 'xmbhyc', 'jyzpl': 'jyzps', 'bjdsyc': 'dsyc', 'gjtbs': 'gjbs',
    #                 'head': 'wdaqm'}
    # 1.修改xml文件下的类别名，可能有错误的或者想改的新的名字
    # check_img_xml(path, replace_dict)

    # # 每一类别的图像个数（训练集大小）
    # 原来数据集命名
    # class_img = {'wcgz': 0, 'xy': 0, 'wdaqm': 0, 'bpmh': 0, 'bpps': 0, 'gbps': 0, 'nc': 0, 'gkxfw': 0, 'xmbhyc': 0,
    #            'dmyw': 0, 'gjbs': 0, 'gjtps': 0,
    #            'hxqyfywyc': 0, 'wkps': 0, 'dsyc': 0, 'helmet': 0, 'jyzps': 0, 'bjzc': 0}
    # # 训练集中每一类别的总体目标个数
    # pro_num = {'wcgz':0, 'xy':0, 'wdaqm':0, 'bpmh':0, 'bpps':0, 'gbps':0, 'nc':0, 'gkxfw':0, 'xmbhyc':0, 'dmyw':0, 'gjbs':0, 'gjtps':0,
    #            'hxqyfywyc':0, 'wkps':0, 'dsyc':0, 'helmet':0, 'jyzps':0, 'bjzc':0}

    # 图像类别名
    classes = {"bj_bpmh", "bj_bpps", "bj_wkps", "jyz_pl", "sly_dmyw", "hxq_gjtps", "hxq_gjbs",
                 "xmbhyc", "yw_gkxfw", "yw_nc", "bjdsyc", "wcaqm", "wcgz", "xy", "ywzt_yfyc", "kgg_ybh", "gbps"}
    # 图像每个类个数
    class_img = {"bj_bpmh": 0, "bj_bpps": 0, "bj_wkps": 0, "jyz_pl": 0, "sly_dmyw": 0, "hxq_gjtps": 0, "hxq_gjbs": 0,
    "xmbhyc": 0, "yw_gkxfw": 0, "yw_nc": 0, "bjdsyc": 0, "wcaqm": 0, "wcgz": 0, "xy": 0, "ywzt_yfyc": 0, "kgg_ybh": 0, "gbps": 0}
    # 每个类别目标个数
    pro_num = {"bj_bpmh": 0, "bj_bpps": 0, "bj_wkps": 0, "jyz_pl": 0, "sly_dmyw": 0, "hxq_gjtps": 0, "hxq_gjbs": 0,
    "xmbhyc": 0, "yw_gkxfw": 0, "yw_nc": 0, "bjdsyc": 0, "wcaqm": 0, "wcgz": 0, "xy": 0, "ywzt_yfyc": 0, "kgg_ybh": 0, "gbps": 0}
    # 需要修改的xml文件夹路径
    path = "E:/Datasets/biandianzhan1/train/annotations/"
    # 2.统计每个类别的目标个数
    count_img_opj(path, classes, class_img, pro_num)
    # # count_img_opj_tree(path, classes, class_img, pro_num)

    # 3.计算
    # old datasets
    # class_img1 = {'wcgz': 48, 'xy': 22, 'wdaqm': 48, 'bpmh': 852, 'bpps': 170, 'gbps': 201, 'nc': 316, 'gkxfw': 752, 'xmbhyc': 486, 'dmyw': 56, 'gjbs': 1417, 'gjtps': 53, 'hxqyfywyc': 681, 'wkps': 68, 'dsyc': 305, 'helmet': 42, 'jyzps': 7, 'bjzc': 0}
    # class_img2 = {'wcgz': 181, 'xy': 57, 'wdaqm': 64, 'bpmh': 579, 'bpps': 180, 'gbps': 118, 'nc': 284, 'gkxfw': 636, 'xmbhyc': 428, 'dmyw': 35, 'gjbs': 1559, 'gjtps': 70, 'hxqyfywyc': 602, 'wkps': 153, 'dsyc': 127, 'helmet': 226, 'jyzps': 20, 'bjzc': 0}
    # class_img3 = {'wcgz': 552, 'xy': 44, 'wdaqm': 165, 'bpmh': 1790, 'bpps': 342, 'gbps': 287, 'nc': 450, 'gkxfw': 468, 'xmbhyc': 428, 'dmyw': 443, 'gjbs': 1052, 'gjtps': 22, 'hxqyfywyc': 240, 'wkps': 243, 'dsyc': 101, 'helmet': 1554, 'jyzps': 153, 'bjzc': 0}
    # class_img4 = {'wcgz': 0, 'xy': 0, 'wdaqm': 0, 'bpmh': 163, 'bpps': 96, 'gbps': 0, 'nc': 340, 'gkxfw': 224, 'xmbhyc': 0, 'dmyw': 242, 'gjbs': 3, 'gjtps': 0, 'hxqyfywyc': 3, 'wkps': 27, 'dsyc': 1, 'helmet': 0, 'jyzps': 122, 'bjzc': 0}
    # class_img5 = {'wcgz': 639, 'xy': 2150, 'wdaqm': 2481, 'bpmh': 0, 'bpps': 0, 'gbps': 0, 'nc': 0, 'gkxfw': 0, 'xmbhyc': 0, 'dmyw': 0, 'gjbs': 0, 'gjtps': 0, 'hxqyfywyc': 0, 'wkps': 0, 'dsyc': 0, 'helmet': 0, 'jyzps': 0, 'bjzc': 0}
    # class_img6 = {'wcgz': 7573, 'xy': 0, 'wdaqm': 5785, 'bpmh': 0, 'bpps': 0, 'gbps': 0, 'nc': 0, 'gkxfw': 1, 'xmbhyc': 13, 'dmyw': 0, 'gjbs': 0, 'gjtps': 0, 'hxqyfywyc': 0, 'wkps': 0, 'dsyc': 0, 'helmet': 18967, 'jyzps': 0, 'bjzc': 0}



    # # # new_data统计目标和图像个数
    # class_img1 =  {'bj_bpmh': 719, 'bj_bpps': 483, 'bj_wkps': 353, 'jyz_pl': 389, 'sly_dmyw': 721, 'hxq_gjtps': 90, 'hxq_gjbs': 1066, 'xmbhyc': 362,
    #                'yw_gkxfw': 429, 'yw_nc': 419, 'bjdsyc': 514, 'wcaqm': 387, 'wcgz': 528, 'xy': 353, 'ywzt_yfyc': 126, 'kgg_ybh': 36, 'gbps': 300}
    #
    # class_img2 =  {'bj_bpmh': 109, 'bj_bpps': 211, 'bj_wkps': 128, 'jyz_pl': 0, 'sly_dmyw': 0, 'hxq_gjtps': 1, 'hxq_gjbs': 74, 'xmbhyc': 6,
    #                'yw_gkxfw': 250, 'yw_nc': 415,'bjdsyc': 143, 'wcaqm': 80, 'wcgz': 133, 'xy': 225, 'ywzt_yfyc': 201, 'kgg_ybh': 20, 'gbps': 268}
    # # class_img3 = {'bj_bpmh': 109, 'bj_bpps': 211, 'bj_wkps': 128, 'jyz_pl': 0, 'sly_dmyw': 0, 'hxq_gjtps': 1,
    # #             'hxq_gjbs': 74, 'xmbhyc': 6, 'yw_gkxfw': 250, 'yw_nc': 415,
    # #             'bjdsyc': 143, 'wcaqm': 80, 'wcgz': 133, 'xy': 225, 'ywzt_yfyc': 201, 'kgg_ybh': 20, 'gbps': 268}
    #
    # class_list = []
    # class_list.extend((class_img1, class_img2))
    #
    # pro_num1 = {'bj_bpmh': 613, 'bj_bpps': 283, 'bj_wkps': 293, 'jyz_pl': 146, 'sly_dmyw': 633, 'hxq_gjtps': 58,
    #           'hxq_gjbs': 832, 'xmbhyc': 294, 'yw_gkxfw': 73, 'yw_nc': 199,
    #           'bjdsyc': 330, 'wcaqm': 325, 'wcgz': 418, 'xy': 312, 'ywzt_yfyc': 25, 'kgg_ybh': 152, 'gbps': 240}
    # pro_num2 = {'bj_bpmh': 146, 'bj_bpps': 220, 'bj_wkps': 102, 'jyz_pl': 264, 'sly_dmyw': 200, 'hxq_gjtps': 47,
    #           'hxq_gjbs': 267, 'xmbhyc': 83, 'yw_gkxfw': 386, 'yw_nc': 243,
    #           'bjdsyc': 298, 'wcaqm': 157, 'wcgz': 258, 'xy': 70, 'ywzt_yfyc': 101, 'kgg_ybh': 162, 'gbps': 117}
    # # pro_num3 = {'bj_bpmh': 110, 'bj_bpps': 220, 'bj_wkps': 128, 'jyz_pl': 0, 'sly_dmyw': 0, 'hxq_gjtps': 1,
    # #           'hxq_gjbs': 75, 'xmbhyc': 6, 'yw_gkxfw': 270, 'yw_nc': 441,
    # #           'bjdsyc': 161, 'wcaqm': 85, 'wcgz': 139, 'xy': 225, 'ywzt_yfyc': 205, 'kgg_ybh': 48, 'gbps': 297}
    # obj_num_list = []
    # obj_num_list.extend((pro_num1, pro_num2))
    #
    # dict_add(class_list, obj_num_list)


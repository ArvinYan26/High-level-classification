#-*- coding: UTF-8 -*-

from ctypes import *
import math
import random
import cv2 as cv
import os
import xml
import sys


def sample(probs):
    s = sum(probs)
    probs = [a / s for a in probs]
    r = random.uniform(0, 1)
    for i in range(len(probs)):
        r = r - probs[i]
        if r <= 0:
            return i
    return len(probs) - 1


def c_array(ctype, values):
    arr = (ctype * len(values))()
    arr[:] = values
    return arr


class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]


class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int)]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]


class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]


# lib = CDLL("/home/pjreddie/documents/darknet/libdarknet.so", RTLD_GLOBAL)
lib = CDLL("/home/Sxin/work/darknet/libdarknet.so", RTLD_GLOBAL)
lib.network_width.argtypes = [c_void_p]
lib.network_width.restype = c_int
lib.network_height.argtypes = [c_void_p]
lib.network_height.restype = c_int

predict = lib.network_predict
predict.argtypes = [c_void_p, POINTER(c_float)]
predict.restype = POINTER(c_float)

set_gpu = lib.cuda_set_device
set_gpu.argtypes = [c_int]

make_image = lib.make_image
make_image.argtypes = [c_int, c_int, c_int]
make_image.restype = IMAGE

get_network_boxes = lib.get_network_boxes
get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int)]
get_network_boxes.restype = POINTER(DETECTION)

make_network_boxes = lib.make_network_boxes
make_network_boxes.argtypes = [c_void_p]
make_network_boxes.restype = POINTER(DETECTION)

free_detections = lib.free_detections
free_detections.argtypes = [POINTER(DETECTION), c_int]

free_ptrs = lib.free_ptrs
free_ptrs.argtypes = [POINTER(c_void_p), c_int]

network_predict = lib.network_predict
network_predict.argtypes = [c_void_p, POINTER(c_float)]

reset_rnn = lib.reset_rnn
reset_rnn.argtypes = [c_void_p]

load_net = lib.load_network
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

do_nms_obj = lib.do_nms_obj
do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

do_nms_sort = lib.do_nms_sort
do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

free_image = lib.free_image
free_image.argtypes = [IMAGE]

letterbox_image = lib.letterbox_image
letterbox_image.argtypes = [IMAGE, c_int, c_int]
letterbox_image.restype = IMAGE

load_meta = lib.get_metadata
lib.get_metadata.argtypes = [c_char_p]
lib.get_metadata.restype = METADATA

load_image = lib.load_image_color
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE

rgbgr_image = lib.rgbgr_image
rgbgr_image.argtypes = [IMAGE]

predict_image = lib.network_predict_image
predict_image.argtypes = [c_void_p, IMAGE]
predict_image.restype = POINTER(c_float)


def classify(net, meta, im):
    out = predict_image(net, im)
    res = []
    for i in range(meta.classes):
        res.append((meta.names[i], out[i]))
    res = sorted(res, key=lambda x: -x[1])
    return res


def detect(net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
    im = load_image(image, 0, 0)
    num = c_int(0)
    pnum = pointer(num)
    predict_image(net, im)
    dets = get_network_boxes(net, im.w, im.h, thresh, hier_thresh, None, 0, pnum)
    num = pnum[0]
    if (nms): do_nms_obj(dets, num, meta.classes, nms);

    res = []
    for j in range(num):
        for i in range(meta.classes):
            if dets[j].prob[i] > 0:
                b = dets[j].bbox
                res.append((meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h)))
    res = sorted(res, key=lambda x: -x[1])
    free_image(im)
    free_detections(dets, num)
    return res

def xml_show(AnnoPath, img_name, img):

    # imagelist = os.listdir(ImgPath)
    # for image in imagelist:
    #     image_pre, ext = os.path.splitext(image)
        #print (image_pre)
        #imgfile = ImgPath + image
        #将标注信息写在
    #print("img_name:", img_name)
    name, ext = os.path.splitext(img_name)    #将l-3.jpg分割成l-3和jpg
    xmlfile = AnnoPath + name + '.xml'
    #print(image, xmlfile)
    # 打开xml文档
    DOMTree = xml.dom.minidom.parse(xmlfile)
    # 得到文档元素对象
    collection = DOMTree.documentElement
    # 读取图片
    #img = cv.imread(imgfile)

    #filenamelist = collection.getElementsByTagName("filename")
    #filename = filenamelist[0].childNodes[0].data
    #print(filename)
    # 得到标签名为object的信息
    objectlist = collection.getElementsByTagName("object")

    all_coor = []
    for objects in objectlist:
        # 每个object中得到子标签名为name的信息
        namelist = objects.getElementsByTagName('name')
        # 通过此语句得到具体的某个name的值
        objectname = namelist[0].childNodes[0].data

        #print("name:", str(objectname))
        bndbox = objects.getElementsByTagName('bndbox')
        # print(bndbox)
        coordinate = []
        coordinate.append(str(objectname))

        for box in bndbox:
            x1_list = box.getElementsByTagName('xmin')
            x1 = int(x1_list[0].childNodes[0].data)
            coordinate.append(x1)
            y1_list = box.getElementsByTagName('ymin')
            y1 = int(y1_list[0].childNodes[0].data)
            coordinate.append(y1)
            x2_list = box.getElementsByTagName('xmax')   #注意坐标，看是否需要转换
            x2 = int(x2_list[0].childNodes[0].data)
            coordinate.append(x2)
            y2_list = box.getElementsByTagName('ymax')
            y2 = int(y2_list[0].childNodes[0].data)
            coordinate.append(y2)
            cv.rectangle(img, (x1, y1), (x2, y2), (50, 205, 50), thickness=2)  #(50, 205, 50)green
            cv.putText(img, objectname, (x1, y1), cv.FONT_HERSHEY_COMPLEX, 1, (50, 205, 50),
                    thickness=2)
            # cv.imshow('head', img)
   
        all_coor.append(coordinate)

    all_coor.sort(key=first, reverse=False) 
    #cv.imwrite(save_path + img_name, img)   #save picture
    #print(all_coor)    
    return all_coor, img

def generate_xml_pre(img, img_name, save_ann_path, box):
    #图片输入路径,原有的基础上添加的脚本
 
    name1 = img_name.split('.', 3)[0]
    [height, width, c] = img.shape
    doc = Document()      #xml base
    root=doc.createElement('annotation')
    doc.appendChild(root)

    annotation1=doc.createElement('folder')
    annotation1.appendChild(doc.createTextNode('test_none'))

    annotation2=doc.createElement('filename')
    annotation2.appendChild(doc.createTextNode(img_name))

    annotation3=doc.createElement('path')
    name9 = img_name   #img path,you can give the path by yourself
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

    for i,bbox in enumerate(box):
        #创建三级节点，循环添加
        annotation6="annotation6"+str(i)
        print(annotation6)
        annotation6=doc.createElement('object')
        name=doc.createElement('name')
        name.appendChild(doc.createTextNode("palm")) #添加类别名
        #创建一个带着文本节点的子节点
        ceo1=doc.createElement('pose')
        ceo1.appendChild(doc.createTextNode("Unspecified"))
        ceo2=doc.createElement('truncated')
        ceo2.appendChild(doc.createTextNode('0'))
        ceo3=doc.createElement('difficult')
        ceo3.appendChild(doc.createTextNode('0'))

        ceo4 = doc.createElement('bndbox')

        #print bbox[0], type(bbox[0]),
        xmin = bbox[0]
        ymin =  bbox[1] 
        xmax =  bbox[2] 
        ymax =  bbox[3] 

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

        root.appendChild(annotation6)




    #将节点信息添加到roo下
    root.appendChild(annotation1)
    root.appendChild(annotation2)
    root.appendChild(annotation3)
    root.appendChild(annotation4)
    root.appendChild(annotation)
    root.appendChild(annotation5)
    #root.appendChild(annotation6)

    #print(doc.toxml())
    #存成xml文件的位置
    print(save_ann_path,name1)
    filename1= save_ann_path +name1+'.xml'
 
    fp = open(filename1, 'w')
    doc.writexml(fp, indent='', addindent='\t', newl='\n')
    fp.close()

def isPython3():
    """
    判断pyton版本
    """
    if sys.version > '3':
	    return True
    return False

def compute_iou(rec1, rec2):
    """
    computing IoU
    :param rec1: (y0, x0, y1, x1), which reflects
            (top, left, bottom, right)
    :param rec2: (y0, x0, y1, x1)
    :return: scala value of IoU
    """
    # computing area of each rectangles
    S_rec1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
    S_rec2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])
 
    # computing the sum_area
    sum_area = S_rec1 + S_rec2
 
    # find the each edge of intersect rectangle
    y1max = max(rec1[1], rec2[1])    #框的左上角的y坐标
    y2min = min(rec1[3], rec2[3])    #框的右下角的y坐标
    x1max = max(rec1[0], rec2[0])    #框的左上角的x坐标
    x2min = min(rec1[2], rec2[2])    #框的右下角的x坐标
    
    # judge if there is an intersect(交集)
    if y2min >= y1max and x2min >= x1max:    #包括交集和子集
        intersect = (y2min - y1max) * (x2min - x1max)
        ver = isPython3    #判断python版本

        if ver == True:
            print("ver:", ver)
            result = (intersect / (sum_area - intersect))*1.0
        else:
            print("version is 2")
            result = float(intersect) / (sum_area - intersect)
    else:
        result = 0

    return result

def select_pro_img(coor0, coor1, threshold):
    """
    0：判断预测框和真值框个数是否相等
        False：漏检，有问题
        true：继续
            1：判断是否名字正确
                False：预测类别错误
                True：继续
                    2：计算iou
                        小于阈值：框的大小预测不准确，
                        大于阈值：图像预测正确
    coor0:预测出来的类别和框位置
    coor1:原始的打标乱的位置
    iou：判断阈值
    """
    if len(coor0) == len(coor1):
        for i in range(len(coor0)):
            if coor0[i][0] == coor1[i][0]:
                # print("coor_information:", type(coor0), coor1)
                rec1, rec2 = coor0[i][1:], coor1[i][1:]
                print("coor_information:", type(rec1), type(rec2))
                print("coor_information:", rec1, rec2)
                iou = compute_iou(rec1, rec2)
                print("iou:", iou)
                if iou < threshold:
                    print("hello0")
                    return False
            else:
                print("hello1")
                return False
    else:
        print("hello2")
        return False        

def first(elem):  
    """
    按表第一个元素排序
    elem:列表元素
    """
    return elem[1] 

def tuple_list(l):
    """
    l = (("one", (6, 2, 4, 4)), ("two", (3, 4, 6, 9)), ("one", (4, 5, 6, 8)))
    转化成 
    l = [['two', 3, 4, 6, 9], ['one', 4, 5, 6, 8], ['one', 6, 2, 4, 4]]
    """
    l_new = []
    for i in [list(x) for x in l]:
        #print("i[0], i[1]:", i[0], i[1])
        s = []
        s.append(i[0])
        # 将第二个元素tuple内的
        #print("i[1]:", i[1])
        for x in i[1]:
            #print(i[1])
            s.append(x)
        # print(s)
        l_new.append(s)
    #print("l_new:")
    # print(len(l_new[0]))    
    l_new.sort(key=first, reverse=True)  #默认是顺序

    return l_new 

if __name__ == "__main__":
    net = load_net(
        "/home/Sxin/work/darknet/gesture/v5-8/tiny_gesture_lite_5_8.cfg",
        "/home/Sxin/work/darknet/gesture/v5-8/tiny_gesture_lite_5_8_100000.weights", 
        0)
    meta = load_meta("/home/Sxin/work/darknet/gesture/v5-8/gesture.data")
    img_path = "/home/Sxin/work/darknet/gesture/data/v5-8/Validation_data/JPEGImages/"
    ann_path = "/home/Sxin/work/darknet/gesture/data/v5-8/Validation_data/Annotations/" #原始图像的Annntations
    
    path0 = "/home/Sxin/work/darknet/gesture/only_pre/"    #预测出来的图像保存位置
    path2 = "/home/Sxin/work/darknet/gesture/only_pre2/"    #预测出来的图像保存位置,重复保存
    
    path1 = "/home/Sxin/work/darknet/gesture/ann_grou_imgs/"  #真值框和预测框在一起的图像保存位置
    img_save_path = "/home/Sxin/work/darknet/gesture/pre_img/"  #存储最终预测不正确的图像

    # threshold = 0.5  #判断是否交集的iou阈值    
    # #plot predict box

    # count = 0 #预测错误的图像个数
    # for filename in os.listdir(img_path):
    #     print("filename:", filename)
    #     r = detect(net, meta, img_path + filename)
    #     #print "r:", r
    #     img = cv.imread(img_path + filename) 
    #     all_coor = []    #预测图像的类别和预测框
    #     for i, item in enumerate(r):
    #         coor = []
    #         pre_name, bbox = item[0], item[2]
    #         coor.append(pre_name)  #将名字添加到第一层列表
            
    #         #print("pre_info:", pre_name, bbox)
    #         #print(pre_name, bbox)
    #         #print pre_name, type(pre_name)
    #         #break
    #         x1 = int(round(bbox[0]) - round((bbox[2] / 2)))   
    #         y1 = int(round(bbox[1] - round(bbox[3] / 2)))
    #         x2 = int(round(bbox[0] + round(bbox[2] / 2)))
    #         y2 = int(round(bbox[1] + round(bbox[3] / 2)))

    #         # 将坐标存储下来
    #         coor.append(x1)
    #         coor.append(y1)
    #         coor.append(x2)
    #         coor.append(y2)

    #         #all_coor = tuple(coor)
    #         all_coor.append(coor)
    #         #print("coor:", coor)
    #         cv.rectangle(img, (x1, y1), (x2, y2), (50, 50, 255), 2)
    #         cv.putText(img, pre_name, (x1, y1), cv.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255),
    #                    thickness=2)
    #         #print("coor_info:", all_coor[0], all_coor[1])
            
    #         #重复性保存框
    #         # print img
    #         # print path2 + filename
    #         cv.imwrite(path2 + filename, img)

    #     if len(all_coor) > 1:
    #          all_coor.sort(key=first, reverse=False)
    #     #将所有预测的图像保存下来
       
    #     cv.imwrite(path0 + filename, img)
        
    #     #将图像真值框画在预测出来的图像上面
    #     coor1, img = xml_show(ann_path, filename, img)
    #     #保存所有的预测图像和真值框图像
        
    #     cv.imwrite(path1 + filename, img)

    #     # 将预测错误的图像画挑出来
    #     print("all_coor, coor1:", all_coor, coor1)
    #     result = select_pro_img(all_coor, coor1, threshold)   #all_coor:预测类别和预测框， coor1：真值框和类别
    #     print("result:", result)
    #     print("="*100) 
    #     if result == False:
    #         count += 1
    #         # print("hello")
    #         # 保存最终挑出来的预测错误的图像
    #         cv.imwrite(img_save_path + filename, img)

    # print("count:", count)




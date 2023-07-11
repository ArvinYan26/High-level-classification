import xml.dom.minidom    #获取xml文件标注信息
import os
import cv2 as cv
import time


def xml_show(img_path, img_save_path):
    imagelist = os.listdir(img_path)
    print(imagelist)

    if not os.path.exists(img_save_path):
        os.makedirs(img_save_path)

    for img_name in imagelist:
        print("image_name:", img_name)
        if img_name.endswith(".jpeg"):

            # image_pre, ext = os.path.splitext(img_name)
            # print (type(img_name))
            imgfile = img_path + img_name
            # 将标注信息写在
            # print("imgfile", imgfile)
            name, ext = os.path.splitext(img_name)  # 将l-3.jpg分割成l-3和jpg
            xmlfile = img_path + name + '.xml'
            # print(imgfile, xmlfile)
            # 打开xml文档
            DOMTree = xml.dom.minidom.parse(xmlfile)
            # 得到文档元素对象
            collection = DOMTree.documentElement
            # 读取图片
            img = cv.imread(imgfile)
            # print(img.size)

            # cv.imshow("image", img)

            # filenamelist = collection.getElementsByTagName("filename")
            # filename = filenamelist[0].childNodes[0].data
            # 得到标签名为object的信息
            objectlist = collection.getElementsByTagName("object")

            all_coor = []
            for objects in objectlist:
                # 每个object中得到子标签名为name的信息
                namelist = objects.getElementsByTagName('name')
                # 通过此语句得到具体的某个name的值
                objectname = namelist[0].childNodes[0].data
                # print(objectname, type(objectname))
                ob_name = objectname.split("_")[1]
                # print("name:", str(objectname), str(ob_name))
                bndbox = objects.getElementsByTagName('bndbox')
                # print(bndbox)
                coordinate = []
                coordinate.append(str(ob_name))

                for box in bndbox:
                    x1_list = box.getElementsByTagName('xmin')
                    x1 = int(x1_list[0].childNodes[0].data)
                    coordinate.append(x1)
                    y1_list = box.getElementsByTagName('ymin')
                    y1 = int(y1_list[0].childNodes[0].data)
                    coordinate.append(y1)
                    x2_list = box.getElementsByTagName('xmax')  # 注意坐标，看是否需要转换
                    x2 = int(x2_list[0].childNodes[0].data)
                    coordinate.append(x2)
                    y2_list = box.getElementsByTagName('ymax')
                    y2 = int(y2_list[0].childNodes[0].data)
                    coordinate.append(y2)
                    cv.rectangle(img, (x1, y1), (x2, y2), (50, 205, 50), thickness=1)  # (50, 205, 50)green
                    cv.putText(img, ob_name, (x1, y1), cv.FONT_HERSHEY_COMPLEX, 0.5, (50, 205, 50),
                               thickness=2)
                    # cv.imshow('head', img)

                # all_coor.append(coordinate)

            # all_coor.sort(key=first, reverse=False)
            cv.imwrite(img_save_path + img_name, img)   #save picture
            # print(all_coor)
        # return all_coor, img


if __name__ == '__main__':
    start_time = time.time()

    img_path = "E:/CompanyDocuments/PonyRobot/5.station_datasets/HuangBu/167_protect/20220826/label/"
    img_save_path = "E:/CompanyDocuments/PonyRobot/5.station_datasets/HuangBu/167_protect/20220826/result_label/"
    print("start")
    xml_show(img_path, img_save_path)
    end_time = time.time()

    print("spent_time:", end_time - start_time)
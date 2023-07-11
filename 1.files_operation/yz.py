import cv2
from PIL import Image

def yz(imgname):
    original_image = cv2.imread(imgname)
    image = original_image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = cv2.Canny(blurred, 120, 255, 1)

    # 找到图片中的轮廓
    cnts = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # 按照面积将所有轮廓逆序排序
    contours2 = sorted(cnts, key=lambda a: cv2.contourArea(a), reverse=True)
    ROI_number = 0
    for c in contours2:
        area = cv2.contourArea(c)
        print(area)
        # 只抠面积大于1200的轮廓，一般印章的轮廓面积比较大，可根据实际情况调整
        if area < 200:
            break
        print("select")
        x, y, w, h = cv2.boundingRect(c)
        # 调整裁剪的位置，避免印章的边缘缺失
        x -= 20
        y -= 20
        w += 40
        h += 40
        cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 1)
        ROI = original_image[y:y + h, x:x + w]
        # cv2.imshow("ROI", ROI)
        img_name = imgname[0: imgname.rindex(".")] + '_{}.jpg'.format(ROI_number)
        print(img_name)
        # cv2.imshow("zhang", img_name)
        # cv2.waitKey(10)
        # cv2.imwrite(img_name, ROI)

        pic = Image.open(img_name)
        # 转为RGBA模式
        pic = pic.convert('RGBA')
        width, height = pic.size
        # 获取图片像素操作入口
        array = pic.load()
        print(array)
        for i in range(width):
            for j in range(height):
                # 获得某个像素点，格式为(R, G, B, A)元组
                pos = array[i, j]
                # RGB三者都大于240(很接近白色了)
                isEdit = (sum([1 for x in pos[0:3] if x > 240]) == 3)
                if isEdit:
                    # 更改为透明
                    array[i, j] = (255, 255, 255, 0)

        # 保存图片
        print(img_name)
        pic.save(img_name)
        ROI_number += 1

# image_path = "zhang.jpg"
# yz(image_path)

#!/usr/bin/env python3
# -*- coding:utf8 -*-

import os

from PIL import Image
im = Image.open('zhang.jpg')  # 打开图片
pix = im.load()  # 导入像素
width = im.size[0]  # 获取宽度
height = im.size[1]  # 获取长度

dir = [(1, 0), (0, -1), (-1, 0), (0, 1)]


def is_red(r, g, b):
    """
    判断是否为红色
    """
    return r > 200 and g < 200 and b < 200


pixel_list = []

for x in range(width):
    for y in range(height):

        pixel = im.getpixel((x, y))
        r, g, b = pixel
        a = 1
        if len(pixel) > 3:
            a = pixel[3]

        if a == 0: # 如果当前像素是透明的，则保持
            pixel_list.append(((x, y), (0, 0, 0, 0)))
        elif r == g == b: # 如果当前颜色是灰色，则删除
            pixel_list.append(((x, y), (0, 0, 0, 0)))
        elif is_red(r, g, b): # 如果当前颜色是红色，则保留
            pixel_list.append(((x, y), (r, g, b, a)))
        elif r >= 220 and g >= 220 and b >= 220: # 如果当前颜色接近白色，则删除
            pixel_list.append(((x, y), (0, 0, 0, 0)))
        else:
            # 取周围像素值来决定当前颜色
            color = (0, 0, 0, 0)
            count = 0
            for d in dir:
                nx, ny = x + d[0], y + d[1]
                if nx >= 0 and nx < width and ny >= 0 and ny < height:
                    count += 1
                    nc = im.getpixel((nx, ny))

                    if len(nc) > 3 and nc[3] == 0:
                        color = (0, 0, 0, 0)
                        break
                    elif is_red(nc[0], nc[1], nc[2]):
                        color = nc
                        break

            pixel_list.append(((x, y), color))

for item in pixel_list:
    im.putpixel(item[0], item[1])

im = im.convert('RGBA')
im.save('ret.png')
import os
import cv2
"""
def IsValidImage(img_path):
     
    判断文件是否为有效（完整）的图片
    :param img_path:图片路径
    :return:True：有效 False：无效
     
    bValid = True
    try:
        Image.open(img_path).verify()
    except:
        bValid = False
    return bValid
"""
def transimg(img_path):
    """
    转换图片格式,图片编码和图片名字必须对应，如果不对应，后期数据集或者其他操作会出现一些问题，乱码或者打不开
    :param img_path:图片路径
    :return: True：成功 False：失败
    """
    folderlist = os.listdir(img_path)  # 文件夹下所有的子文件夹名（列表形式）
    count = 0
    for folder in folderlist:
        print(folder)
        inner_path = os.path.join(img_path, folder)
        filelist = os.listdir(inner_path)
        for item in filelist:
            or_name = img_path + folder+'/'+item    #原图像文件是路径加文件名，这才是完整的文件读取的内容
            name0 = item.split(".")[0]
            new_name = img_path + folder + '/' + name0+'.jpg'
            img = cv2.imread(or_name)   #用cv2将文件读取出来
            cv2.imwrite(new_name, img)   #然后用从按照重命名的图片格式的编码方式将原文件改写成名字和图像格式对应的图像

    return True

if __name__ == '__main__':
    #img_path = 'C:/Users/Yan/Desktop/Gesture_category/two/'
    img_path = 'C:/Users/Yan/Desktop/new_name_img/'
    transimg(img_path)

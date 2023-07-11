import os
import imghdr
import cv2

def is_type_wrong(path):
    """
    判断图片格式和名字命名的格式是否对应，如果不对应，
    就修改成名字和图片编码格式相同的形式
    :param path:原文件路径
    :return:
    """
    fillist = os.listdir(path)
    count = 0
    for i, file in enumerate(fillist):
        #print("file:", file)
        img = path + '/' + file   #图片文件（可读，可写）
        #print("img:", img)
        real_type = imghdr.what(img)
        img_name = os.path.splitext(file)[0]

        #print('real_type:', real_type)

        if real_type == 'png' or real_type == 'gif':
        #if not real_type == 'jpg':  #方法一样，但是很费时
            img = cv2.imread(img)
            new_name = path + '/' + img_name + '.jpg'  #新的路径加名字
            #print('new_name:', new_name)
            cv2.imwrite(new_name, img)    #把图像写到新的路径下的新名字，如果修改后的文件和原文件名字相同，就会覆盖原文件
            type_a = imghdr.what(new_name)
            #print(type_a)
            count += 1
    print(count, 'done')

if __name__ == '__main__':
    path = 'E:/PycharmProjects/datasets/final_dataset/merger/bymyself/13.thumbs up'
    is_type_wrong(path)







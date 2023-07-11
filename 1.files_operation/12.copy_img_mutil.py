import os
import shutil



def copy_img_mutil(or_path, new_img_path):
    """
    文件夹下多个子文件夹下的所有图片
    :param or_path:源文件夹
    :param new_path: 新文件夹
    :return:
    """
    for root, dirs, files in os.walk(or_path):
        # print("root:", root)
        # print("dirs:", dirs)
        # print("files:", files)
        for id, item in enumerate(files):
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
    print("done")

if __name__ == '__main__':
    or_path = 'E:/CompanyDocuments/PonyRobot/3.LearningFiles/项目学习/2.变电站识别结果/旭山变电站/保护室/20220814/'  # 表示需要命名处理的文件夹
    new_img_path = 'E:/CompanyDocuments/PonyRobot/3.LearningFiles/项目学习/2.变电站识别结果/旭山变电站/保护室/20220814/JPEGImages/'  # 创建的新文件夹
    copy_img_mutil(or_path, new_img_path)
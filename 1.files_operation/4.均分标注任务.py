
import os
import shutil
import traceback


def split_images(path, split_path, name_dir_list):
    '''
    按文件夹命名划分需要标注文件夹
    :param path: 源图片路径
    :param split_path: 存放父目录
    :param name_dir_list: 文件夹命名
    :return:
    '''

    dir_dict = {}

    try:

        for j, dir_name in enumerate(name_dir_list):
            dir = os.path.join(split_path, dir_name)
            if os.path.isdir(dir):
                shutil.rmtree(dir)   #递归删除一个目录以及目录下的所有内容
            os.mkdir(dir)
            dir_dict[dir_name] = dir

        count = 0
        for i, file in enumerate(os.listdir(path)):
            new_name = os.path.join(path, 'i_'+str(count).zfill(5)+".jpg")
            old_name = os.path.join(path, file)
            print('old_name, new_name', old_name, new_name)
            os.rename(old_name, new_name)
            print(old_name,new_name)

        if count <= 400:
            shutil.copy(new_name, dir_dict[name_dir_list[0]])
        elif 400 < count <= 800:
            shutil.copy(new_name, dir_dict[name_dir_list[1]])
        else:
            shutil.copy(new_name, dir_dict[name_dir_list[3]])

        count += 1

    except Exception as e:
        print(traceback.print_exc())

def split_data_to_people():

    def split_data(path):
        """
        split the data to diferent people
        :param path:original path
        :return:
        """
        path1 = '0/'
        path2 = '1/'
        path3 = '2/'
        count = 0
        for i, file in enumerate(os.listdir(path)):
            print(i)
            new_name = path + '/' + file  # 路径下文件，路径，文件名
            """
            new_name = os.path.join(path, str(i+1633).zfill(5)+".jpg")
            old_name = os.path.join(path, file)
            os.rename(old_name, new_name)

            print('old_name, new_name', old_name, new_name)
            """

            if count <= 400:
                shutil.copy(new_name, path1)
            elif 400 < count <= 800:
                shutil.copy(new_name, path2)
            else:
                shutil.copy(new_name, path3)

            count += 1



if __name__ == '__main__':
    split_data_to_people(path='test_mud') #当前路径夹
    split_images(r'C:\Users\Yan\Desktop\stainsdataset\test_mud',
                 r'C:\Users\Yan\Desktop\stainsdataset\newtest', ['jianglong', 'dongsheng', 'qinxu'])
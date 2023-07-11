"""
提取图像特征，然后生成csv格式的数据集
"""
import os.path
import glob
import cv2
import numpy as np
import pandas as pd
import time
from quadtree import QuadTreeSolution

class ExtractFeatures(object):
    def __init__(self):
        """
        set all the parameters of this project
        """
        self.images_folder = r'../data/images/sclect_datasets'
        # It will make a new file(ft_qt_50_50.csv) automatically
        self.data_save_path = '../data/extract_features/ft_qt_150_150.csv'
        # set the label for each class 0:the first folder; 1:second folder
        self.labels = [0, 1]  # 标签的顺序需要与子文件夹的顺序一致
        # 用于保存特征和标签的列表
        self.features = []
        self.all_labels = []
        # self.count = 0
        # 二值图像的阈值范围100 -- 160， 间隔是10
        self.min_value, self.max_value, self.steps = 100, 160, 10
        self.Threshold = [x for x in range(self.min_value, self.max_value, self.steps)]
        # 设置qudatree算法的参数，最小截止分割像素值，最小截止分割的区域像素值的的方差值
        self.min_pix, self.min_sd, self.num_rank = 1, 60, 7
        self.grid_rank = sorted([self.min_pix * (2 ** i) for i in range(self.num_rank)], reverse=False)

    def fractal_dimension(self, Z, threshold):
        """
        Algorithm for computing the fractal dimension
        """
        # Only for 2d image
        assert(len(Z.shape) == 2) #assert ： 判断语句，如果是二维图像就执行，不是的话，直接报错，不再执行

        # From https://github.com/rougier/numpy-100 (#87)
        def boxcount(Z, k):
            #axis=0, 按列计算， 1：按行计算
            S = np.add.reduceat(
                np.add.reduceat(Z, np.arange(0, Z.shape[0], k), axis=0),
                                   np.arange(0, Z.shape[1], k), axis=1)

            # We count non-empty (0) and non-full boxes (k*k)
            return len(np.where((S > 0) & (S < k*k))[0])
        # Transform Z into a binary array
        Z = (Z < threshold)
        #plt.draw()
        #plt.show()

        # Minimal dimension of image
        p = min(Z.shape)

        # Greatest power of 2 less than or equal to p
        n = 2**np.floor(np.log(p)/np.log(2))

        # Extract the exponent
        n = int(np.log(n)/np.log(2))

        # Build successive box sizes (from 2**n down to 2**1)
        sizes = 2**np.arange(n, 1, -1)

        # Actual box counting with decreasing size
        counts = []
        for size in sizes:
            counts.append(boxcount(Z, size))

        # Fit the successive log(sizes) with log (counts)
        coeffs = np.polyfit(np.log(sizes), np.log(counts), 1)
        return -coeffs[0]
    def process_images(self, folder, label):
        # 遍历文件夹
        # qt_feature_name = None
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            # 判断是否为文件，如果是直接读取，
            if os.path.isfile(file_path):
                if filename.endswith(".jpg") or filename.endswith(".png"):
                    # 读取为灰度图，在这里执行特征提取的代码，得到一个特征向量 feature
                    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                    # dst = cv2.resize(img, (512, 512), interpolation=cv2.INTER_CUBIC)  # interpola：双线性插值方式
                    feature = []
                    for i in self.Threshold:
                        ret, b_img = cv2.threshold(img, i, 255, cv2.THRESH_BINARY)
                        d = self.fractal_dimension(b_img, i)
                        feature.append(d)
                    # extract the feature of the qudatree,
                    # 1:最小截止分割像素大小；60：区域像素值的方差最小截止分割值，满足任意条件都将截止分割
                    s = QuadTreeSolution(img, self.min_pix, self.min_sd)
                    # s = QuadTreeSolution(img, 1) #李根改进，不同级别块，var阈值不同
                    qt_feature = s.extract_img_features(self.grid_rank)
                    # his = s.extract_img_features()
                    feature += qt_feature
                    # img_grid = s.bfs_for_segmentation()  # 得到带分隔线的图
                    # img_data.append(img_grid)  # 存储的原始灰度图像

                    # 将列表转化为特征向量
                    feature = np.array(feature)
                    self.features.append(feature)
                    self.all_labels.append(label)  # 添加对应的标签
            # 如果不是就递归处理文件夹 Process folders recursively
            elif os.path.isdir(file_path):
                # count = self.process_images(folder, label, count)  # 递归处理子文件夹
                self.process_images(folder, label)  # 递归处理子文件夹
    def extract_feature(self):
        # 遍历根文件夹中的子文件夹
        # count = 0
        for i, folder_name in enumerate(sorted(os.listdir(self.images_folder))):
            # 子文件夹路径
            folder_path = os.path.join(self.images_folder, folder_name)
            print(folder_path, self.labels[i])
            if os.path.isdir(folder_path):
                self.process_images(folder_path, self.labels[i])

        # 将特征和标签转换为 NumPy 数组
        features = np.array(self.features)
        all_labels = np.array(self.all_labels)

        # 创建 DataFrame 对象
        df = pd.DataFrame(features)

        # 给每一列指定特征名称
        # feature_names = ['Feature {}'.format(i+1) for i in range(features.shape[1])]
        feature_name = self.Threshold + self.grid_rank
        feature_names = [str(element) for element in feature_name]

        df.columns = feature_names
        # 添加标签列
        df['label'] = all_labels

        # 保存到 CSV 文件
        df.to_csv(self.data_save_path, index=False)



if __name__ == '__main__':
    start_time = time.time()
    # All the relevant parameters are in the class method
    # 图像文件夹路径和对应的标签
    et = ExtractFeatures()
    et.extract_feature()
    end_time = time.time()

    # Print the runtime in seconds
    total_time = end_time - start_time
    print("Program runtime(seconds):{}".format(total_time))

    # Optional: Convert the time to a more friendly format (hours, minutes, seconds)
    hours = int(total_time // 3600)
    minutes = int((total_time % 3600) // 60)
    seconds = int(total_time % 60)
    print("Program runtime(HH:MM:SS):{:02d}：{:02d}：{:02d}".format(hours, minutes, seconds))






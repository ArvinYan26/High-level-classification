from utils import *
from build_network import DataClassification
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

if __name__ == '__main__':
    """
        #单次运行
        train_data, train_target, test_data, test_target = data_segmentation(p=0.1)
        DC = DataClassification(k=8, num_class=2)
        DC.fit(train_data, train_target)
        DC.predict(test_data, test_target)
        acc = DC.score()
        #for i in range(10)
        """
    # 读取 CSV 文件
    df = pd.read_csv('../data/extract_features/ft_qt_150_150.csv')
    # 按类别划分数据
    grouped = df.groupby('Label')
    # 从每个类别中选择前 50 个数据
    sampled_data = []

    # datasets:每一个类别数据集大小,乘上2就是总的数据集)；test_size:测试集大小（从总数据集上抽出来的）
    datasets, test_size = 150, 30
    epochs = 10
    for _, group in grouped:
        # selcet the first 50 samples of each class
        class_data = group.head(datasets)
        sampled_data.append(class_data)
    sampled_df = pd.concat(sampled_data)
    # Count the number of data in each category
    class_counts = sampled_df['Label'].value_counts()
    # print(class_counts)
    # 提取特征和标签
    data = sampled_df.drop('Label', axis=1).values
    data_target = sampled_df['Label'].values

    # print("data:", len(data))
    # print(len(data), data, len(data_target))
    # data normalization
    data = data_preprocess(data)
    print(f"datasets:{len(data)}")

    # # 找到最优的k值
    # k = [i for i in range(1, 21)]
    # print("k:", k)
    # calss_num, method_num = 2, 4
    # ptm = ParameterTuningMethod(data, data_target, k, calss_num, method_num)
    # print("x", ptm.best_parameter)
    # if ptm.best_parameter:
    #     print("ptm.best_parameter:", ptm.best_parameter)

    # 开始测试
    all_acc = []
    # 该方法就是交叉验证，其实，或者成为一致性方法
    for i in range(epochs):
        # single run
        print(f"第--------{i}---------次运行")
        train_data, test_data, train_target, test_target = train_test_split(data, data_target, test_size=test_size, stratify=data_target)
        DC = DataClassification(num_class=2, k=7)
        DC.fit(train_data, train_target)
        DC.predict(test_data, test_target)
        acc = accuracy_score(DC.Y_test, DC.predict_label)
        # acc = DC.score()
        print(f"acc:{acc:.4f}")
        all_acc.append(round(acc, 4))

    # 计算平均值
    # mean_value =
    # 计算标准方差
    # std_value = np.std(all_acc)

    print(f"all_acc:{all_acc}")
    print(f"Average_acc:{np.mean(all_acc):.4f}, Standard Deviation:{np.std(all_acc):.4f}", )
    # print("Standard Deviation:", std_value)



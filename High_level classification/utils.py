from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV, train_test_split
import numpy as np
from sklearn.utils import resample
from build_network import DataClassification
def data_preprocess(data):
    """特征工程（归一化）"""
    # 归一化
    scaler = preprocessing.MinMaxScaler().fit(data)
    data = scaler.transform(data)
    return data

def plot_acc_line(ave_acc):
    x = [i for i in range(1, 12)]
    plt.plot(x, ave_acc, color="#afafff", label="covid3")
    # handlelength:图例线的长度, borderpad：图例窗口大小, labelspacing：label大小， fontsize：图例字体大小
    plt.legend(loc="lower right", handlelength=4, borderpad=2, labelspacing=2, fontsize=12)
    plt.yticks(size=15)  # 设置纵坐标字体信息
    # plt.ylabel("Desmension", fontsize=20)

    # 设置x轴刻度显示值
    # 参数一：中点坐标
    # 参数二：显示值
    plt.xticks(size=15)
    # plt.xlabel("Thershold", fontsize=20)

    plt.xlabel("valuse of the K", size=20)
    plt.ylabel("accuracy", size=20)
    plt.show()

class ParameterTuningMethod(object):
    def __init__(self, X, y, k_values, class_num, m_n):
        self.X = X
        self.y = y
        self.class_num = class_num
        print("self.class_num", self.class_num, m_n)
        self.k_values = k_values
        self.best_parameter = []
        # if函数是判断非零值或者真值，如果是0，就不执行返回的是False
        if m_n:
            print("m_n")
            if m_n == 1:
                self.cross_validation()
            if m_n == 2:
                self.grid_search()
            if m_n == 3:
                self.consistency_based()
            if m_n == 4:
                self.consistency_based()


    def cross_validation(self):
        # 存储每个K值的交叉验证得分
        mean_scores = []
        for k in self.k_values:
            # 创建KNN分类器
            knn = DataClassification(self.class_num, k)
            print(self.class_num)
            # 执行交叉验证并计算平均得分
            scores = cross_val_score(knn, self.X, self.y, cv=5)  # 这里使用5折交叉验证
            mean_scores.append(np.mean(scores))

        # 找到最优K值
        print("mean_scores:", mean_scores)
        best_k = self.k_values[np.argmax(mean_scores)]
        best_score = max(mean_scores)
        print("Best K:", best_k)
        print("Best Score:", best_score)
        self.best_parameter.extend((best_k, best_score))


    def grid_search(self):
        """
        网格搜索（Grid Search）：使用网格搜索方法，在给定的K值范围内，通过交叉验证评估每个K值的性能，并选择具有最佳性能的K值。
        网格搜索方法可以通过Scikit-learn库的GridSearchCV类来实现。
        """
        # 创建KNN分类器
        knn = DataClassification(self.class_num)

        # 定义参数网格
        param_grid = {'n_neighbors': self.k_values}

        # 执行网格搜索
        grid_search = GridSearchCV(knn, param_grid, cv=5)
        grid_search.fit(self.X, self.y)

        # 输出最优参数和得分
        best_k = grid_search.best_params_['n_neighbors']
        best_score = grid_search.best_score_

        print("Best K:", best_k)
        print("Best Score:", best_score)

        self.best_parameter.extend((best_k, best_score))

    def boots_trapping(self):
        """
        自助法（Bootstrapping）：使用自助法来估计不同K值下的模型性能。自助法通过从原始数据集中有放回地抽取样本创建多个训练集，
        然后在每个训练集上构建KNN模型并评估性能。通过平均多个自助样本的性能来选择最优K值。
        此还有一些问题待解决，暂时不使用
        """
        # 定义K值的范围
        k_values = range(1, 21)

        # 存储每个K值的交叉验证得分
        mean_scores = []

        # 执行自助法
        for k in k_values:
            scores = []
            for _ in range(20):  # 重复20次自助采样
                # 进行自助采样
                X_train, y_train = resample(self.X, self.y)

                # 创建KNN分类器
                knn = DataClassification(self.class_num, k)

                # 训练和评估模型
                knn.fit(X_train, y_train)
                score = knn.score()
                scores.append(score)

            # 计算平均得分
            mean_scores.append(np.mean(scores))

        # 找到最优K值
        best_k = k_values[np.argmax(mean_scores)]
        best_score = max(mean_scores)

        print("Best K:", best_k)
        print("Best Score:", best_score)
    def consistency_based(self):
        """
        一致性方法（Consistency-based method）：一致性方法使用不同的K值构建多个KNN模型，并通过比较模型的一致性来选择最优K值。
        一致性可以使用样本分类的变异性或基于重采样的方法来衡量。
        这是一个统称的方法，核心是，用不同的参数创建多个模型，然后测试
        """
        # 存储每个K值的一致性得分
        consistency_scores = {}
        # results = {}
        # 执行一致性方法
        for k in self.k_values:
            scores = []
            for _ in range(20):  # 重复20次
                # 划分训练集和测试集
                X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2)

                # 创建KNN分类器
                knn = DataClassification(self.class_num, k)

                # 训练模型
                knn.fit(X_train, y_train)

                # 预测并计算准确率
                y_pred = knn.predict(X_test, y_test)
                score = accuracy_score(y_test, y_pred)
                scores.append(score)

            # 将得分存储到字典中
            consistency_scores[k] = scores

        # 输出每个K值下的得分
        for k, scores in consistency_scores.items():
            print("K:", k)
            for i, score in enumerate(scores):
                print("Score", i + 1, ":", score)

        # 找到最优K值
        best_k = min(consistency_scores, key=lambda k: np.var(consistency_scores[k]))
        best_scores = consistency_scores[best_k]

        print("Best K:", best_k)
        print("Best Scores:", best_scores)

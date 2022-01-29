import warnings
import matplotlib.pyplot as plt
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier, RandomForestClassifier, ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier
from GetCOVID_19Data1 import get_data
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
import pandas as pd
import numpy as np
from sklearn import preprocessing

warnings.filterwarnings('ignore')


def data_preprocess(data):
    """特征工程（归一化）"""
    # 归一化
    scaler = preprocessing.MinMaxScaler().fit(data)
    data = scaler.transform(data)

    return data

def classification_campare(x_train, y_train, x_test, y_test):
    """
    X, y = make_circles(n_samples=300, noise=0.15, factor=0.5, random_state=233)
    plt.scatter(X[y == 0, 0], X[y == 0, 1])
    plt.scatter(X[y == 1, 0], X[y == 1, 1])
    # plt.show(x_train, X_test, y_train, y_test = train_test_split(X, y)
    """
    #x_train, x_test, y_train, y_test = get_data(percent=0.9)
    #print('X_train.shape=', x_train.shape)
    #print('X_test.shape=', x_test.shape)
    #print(y_test)

    a = []
    print('===========NB==============')
    NB_clf = Pipeline([
            ('sc', StandardScaler()),
            ('clf', GaussianNB())])     # 管道这个没深入理解 所以不知所以然
    NB_clf.fit(x_train, y_train.ravel())  # 利用训练数据进行拟合
    print('NB accuracy={}'.format(NB_clf.score(x_test, y_test)))
    a.append(NB_clf.score(x_test, y_test))
    print('\n')

    print('===========RF==============')
    RF_clf = RandomForestClassifier(n_estimators=100, n_jobs=4, oob_score=True)
    RF_clf.fit(x_train, y_train.ravel())
    #ir = RF_clf.fit(x_train, y_train.ravel())  # 利用训练数据进行拟合
    print('RF accuracy={}'.format(RF_clf.score(x_test, y_test)))
    a.append(RF_clf.score(x_test, y_test))
    print('\n')


    print('===========knn==============')
    knn_clf = KNeighborsClassifier()
    knn_clf.fit(x_train, y_train)
    print('knn accuracy={}'.format(knn_clf.score(x_test, y_test)))
    a.append(knn_clf.score(x_test, y_test))
    print('\n')

    print('===========Decison tree==============')
    DT_clf = DecisionTreeClassifier()  # 所有参数均置为默认状态
    DT_clf.fit(x_train, y_train)
    print('Decison tree accuracy={}'.format(DT_clf.score(x_test, y_test)))
    a.append(DT_clf.score(x_test, y_test))
    print('\n')

    print('===========logistic regression==============')
    log_clf = LogisticRegression()
    log_clf.fit(x_train, y_train)
    print('logistic regression accuracy={}'.format(log_clf.score(x_test, y_test)))
    a.append(log_clf.score(x_test, y_test))
    print('\n')

    print('===========SVM==============')
    svm_clf = SVC()
    svm_clf.fit(x_train, y_train)
    print('SVM accuracy={}'.format(svm_clf.score(x_test, y_test)))
    a.append(svm_clf.score(x_test, y_test))
    print('\n')

    ada_clf = AdaBoostClassifier(DecisionTreeClassifier(),
                                 n_estimators=500,
                                 learning_rate=0.3)

    ada_clf.fit(x_train, y_train)
    print('Adaboost accuracy={}'.format(ada_clf.score(x_test, y_test)))
    a.append(ada_clf.score(x_test, y_test))
    print('\n')

    print('===========MLP(Deep Neural Multilayer Perceptron==============')
    MLP_clf = MLPClassifier(hidden_layer_sizes=(256, 128, 64, 32),
                        activation="relu", random_state=1)
    MLP_clf.fit(x_train, y_train)
    print('MLP accuracy={}'.format(MLP_clf.score(x_test, y_test)))
    a.append(MLP_clf.score(x_test, y_test))
    print('\n')
    print("="*150)
    return a
if __name__ == '__main__':
    #df = pd.read_csv(r"C:\Users\Yan\Desktop\dimension_100_160_10.csv")
    """
    features = list(df.columns)
    features = features[: len(features) - 1]  # 去掉开头和结尾的两列数据
    data = df[features].values.astype(np.float32)
    data_target = np.array(df.target)
    """
    data, data_target = get_data()
    data = data_preprocess(data)
    ave_acc = []
    for i in range(50):
        x_train, x_test, y_train, y_test = train_test_split(data, data_target, test_size=0.2)
        acc = classification_campare(x_train, y_train, x_test, y_test)
        ave_acc.append(acc)

    mean_acc = np.mean(np.array(ave_acc), axis=0) #求每一列的精确度平均值
    var = np.var(np.array(ave_acc), axis=0) #   #求每一列精确度的的方差
    ave_acc.append(mean_acc)
    #print(a)
    #print("%f +- %f", (mean_acc, var))
    print("ave_acc:", np.array(ave_acc))
    print("mean_acc:", mean_acc)
    print("var     :", var)

    """
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
    """

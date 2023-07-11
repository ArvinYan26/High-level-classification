import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer

from sklearn.neighbors import NearestNeighbors
#from test2 import split_data  # test文件中的spli_data函数
import pandas as pd
import time



class DataClassification(object):
    """iris数据集分类"""

    def __init__(self, num_class=None, k=None):
        self.default_k = 6  # 类的默认参数k
        self.num_class = 2
        if k is not None:
            self.k = k  # 使用新的参数k
        else:
            self.k = self.default_k  # 使用类本身的默认参数k

        if num_class is not None:
            self.num_class = num_class  # 使用新的参数k
        else:
            self.num_class = self.num_class  # 使用类本身的默认参数k

        self.num_class = num_class
        self.nbrs = []  # 用来存储是哪个类别网络的nbrs
        self.radius = []  # 用来存储是哪个类别的

        self.net0_measure = []  # 存储每一类别插入Y_items中的数据时的指标
        self.impact0 = []  # storage the impact of the first class
        self.net1_measure = []
        self.impact1 = []
        self.net2_measure = []
        self.G = nx.Graph()

        self.predict_label = []

        # 初始化运行程序，一开始就运行

        self.need_classification = []  # 计算模糊分类节点次数

        # self.accuracy()

    def fit(self, train_data, train_target):

        self.train_data = train_data
        self.train_target = train_target
        self.build_init_network(label=True)

    def KNN(self, nbrs, train_data):
        """
        KNN获取节点邻居和邻居索引
        :param nbrs:
        :param train_data:
        """
        distances, indices = nbrs.kneighbors(train_data)
        return distances, indices

    def get_radius(self, distances):

        return np.median(distances)  # 中位数

    def epsilon_radius(self, nbrs, train_data, radius):
        """

        :param nbrs:
        :param train_data:
        :param radius:
        :return:
        """
        nbrs.set_params(radius=radius)
        nbrs_distances, nbrs_indices = nbrs.radius_neighbors(train_data)

        return nbrs_distances, nbrs_indices

    def max_normalization(self, init_mea, new_mea):
        """
        最大值归一化，将所有数据除以最大值
        :return: 归一化后的数据
        """
        l = []
        l.append(init_mea[0])
        l.append(new_mea[0])
        max_value = max(l)
        init_mea = [round(init_mea[0]/max_value, 3)]
        new_mea = [round(new_mea[0]/max_value, 3)]
        return init_mea, new_mea


    def init_net_measure1(self, G):
        """
        初始化网络measures
        :param G: 构建的网络
        :return:
        """

        measures = {}
        #可通信性（全局）
        c = nx.communicability(G)  # 单个节点measures
        mean_c = {}
        for key in c:
            node_c = []
            dict = c[key]    #切片数字只能是整数，而不是字符串，此处节点是字符串，所以只能先转化为整型。
            for value in dict.values():
                node_c.append(value)
            mean_node_c = np.mean(node_c)
            mean_c[key] = mean_node_c
        l = len(mean_c)
        all_values = sum(mean_c.values())
        average_communicallity = round(all_values/l, 5)
        measures["average_communicallity"] = average_communicallity
        return measures

    def calculate_measure1(self, G):
        """
        :param net: 构建的网络g
        :param nodes: 每一类的网络节点
        :return:
        """
        measures = []
        # 可通信性（全局），计算平均可通信性
        c = nx.communicability(G)  # 单个节点measures
        mean_c = {}
        for key in c:
            node_c = []
            dict = c[key]  # 切片数字只能是整数，而不是字符串，此处节点是字符串，所以只能先转化为整型。
            for value in dict.values():
                node_c.append(value)
            mean_node_c = np.mean(node_c)
            mean_c[key] = mean_node_c
        l = len(mean_c)
        all_values = sum(mean_c.values())
        average_communicallity = round(all_values / l, 5)
        measures.append(average_communicallity)

        return measures

    def calculate_measure(self, G):
        """
        :param net: 构建的网络g
        :param nodes: 每一类的网络节点
        :return:
        """

        measures = []


        # 平均度，平均最短路径，平均聚类系数， 同配性， 传递性
        #1.  平均度
        ave_deg = G.number_of_edges() * 2 / G.number_of_nodes()
        # ave_deg = round(ave_deg, 3)
        measures.append(ave_deg)

        # 2.  平均最短路径长度(需要图是连通的)
        ave_shorest = nx.average_shortest_path_length(G)
        # ave_shorest = round(ave_shorest, 3)
        #print("平均最短路径：", ave_shorest)
        measures.append(ave_shorest)

        # 3.  平均聚类系数
        ave_cluster = nx.average_clustering(G)
        # ave_cluster = round(ave_cluster, 3)
        # print("平均聚类系数：%f" % ave_cluster)
        measures.append(ave_cluster)

        # 4.  度同配系数 Compute degree assortativity of graph
        assortativity = nx.degree_assortativity_coefficient(G)
        # assortativity = round(assortativity, 3)
        # print("同配性：%f" % assortativity)
        measures.append(assortativity)

        # 5.  传递性transitivity：计算图的传递性，g中所有可能三角形的分数。
        tran = nx.transitivity(G)
        # tran = round(tran, 3)
        #print("三角形分数：%f" % tran)
        measures.append(tran)

        #measures = []
        efficiency = nx.global_efficiency(G)
        # efficiency = round(efficiency, 3)
        measures.append(efficiency)

        return measures

    def build_init_network(self, label):
        for index, instance in enumerate(self.train_data):
            self.G.add_node(str(index), value=instance, typeNode="init_net", label=self.train_target[index])
        # 切片范围必须是整型
        temp_nbrs = NearestNeighbors(n_neighbors=self.k, metric='euclidean')
        temp_nbrs.fit(self.train_data)
        self.nbrs.append(temp_nbrs)  # 将每一类的nbrs都添加进列表， 这个
        knn_distances, knn_indices = self.KNN(temp_nbrs, self.train_data)
        temp_radius = self.get_radius(knn_distances)
        self.radius.append(temp_radius)  # 将每一类的radius都添加进radius
        # print("self.radius:", self.radius)
        radius_distances, radius_indices = self.epsilon_radius(temp_nbrs, self.train_data, temp_radius)
        # 添加连边
        for idx, one_data in enumerate(self.train_data):  # 这个语句仅仅是获取索引indx，然后给他连边
            if (len(radius_indices[idx])) > self.k:  # 判断用哪种方法连边构图,因为,adius应用于稠密区域，邻居大于k的话就是稠密
                for indiceNode, indicesNode in enumerate(radius_indices):
                    for tmpi, indice in enumerate(indicesNode):
                        if (str(indice) == str(indiceNode)):
                            continue
                        if (self.G.nodes()[str(indice)]["label"] == self.G.nodes()[str(indiceNode)][
                            "label"] or not label):
                            self.G.add_edge(str(indice), str(indiceNode), weight=radius_distances[indiceNode][tmpi])

            else:
                for indiceNode, indicesNode in enumerate(knn_indices):
                    for tmpi, indice in enumerate(indicesNode):
                        if (str(indice) == str(indiceNode)):
                            continue
                        if (self.G.nodes()[str(indice)]["label"] == self.G.nodes()[str(indiceNode)][
                            "label"] or not label):
                            self.G.add_edge(str(indice), str(indiceNode), weight=knn_distances[indiceNode][tmpi])
        self.merge_components()
        self.G0, self.G1 = self.get_subgraph(self.G)
        # draw graph
        # self.draw_graph(self.G)
        # self.draw_graph(self.G0)
        # self.draw_graph(self.G1)
        #
        # print(self.G0.edges, self.G1.edges)
        # 计算初始子网络的measures,凸显差别
        self.measures0 = self.calculate_measure(self.G0)
        self.measures1 = self.calculate_measure(self.G1)
        # print("measues0:", self.measures0)
        # print("measues1:", self.measures1)
        # self.measures0 = list(self.measures0.values())
        #
        # self.measures1 = list(self.measures1.values())
        # print("measues0:", self.measures0)
        # print("measues1:", self.measures1)



        print("*"*100)

    def draw_graph(self, G):
        plt.figure("Graph", figsize=(8, 8))
        color_map = {0: 'b', 1: 'r'}
        pos = nx.spring_layout(G)
        color_list = [color_map[G.nodes[node]['label']] for node in G.nodes()]

        for index, (node, typeNode) in enumerate(G.nodes(data='typeNode')):
            if (typeNode == 'test'):
                color_list[index] = 'k'
        nx.draw_networkx(G, pos, with_labels=False, node_size=100,
                         node_color=color_list, width=0.2, alpha=0.9)
        plt.show()

    def get_subgraph(self, G):
        """得到各个类别网络中最大的组件"""
        # num = nx.number_connected_components(self.G)
        Gcc = sorted(nx.connected_components(G), key=len, reverse=True)  #Gcc不能全局，因为会变化
        self.G0 = self.G1 = None

        for i in range(len(Gcc)):
            sub_G = G.subgraph(Gcc[i])

            target = sub_G._node[list(sub_G.nodes())[0]]["label"] #子图节点集合中的第一个节点target
            if target == 0:
                if self.G0 is None:
                    self.G0 = sub_G
                    #print("G0:", self.G0.nodes())
                elif self.G0 is not None:
                    continue
            elif target == 1:
                #if count1 > 3:
                #global G1
                if self.G1 is None:
                    self.G1 = sub_G
                    #print("G1:", self.G1.nodes())
                elif self.G1 is not None:
                    continue

            elif not self.G0 and self.G1 is None:
                break

        return self.G0, self.G1

    def merge_components(self):

        """
        合并单节点，小的组件。因为分类阶段不需要合并，所以这个函数需要单独建立
        :param G:
        :return:
        """
        #steps1：对于单节点，计算每一个单节点的最近的一个同类节点，然后连一条边，合并单节点
        for single_node in self.G.nodes():  # 单节点，因为neighbors迭代器用的节点编号的字符串，所以需要转化为字符串
            adj = [n for n in self.G.neighbors(single_node)]  # find the neighbors of the new node
            if len(adj) == 0: #说明是单节点
                all_dist = [] #所有节点对的节点编号和相对应的欧式距离
                for node_id in self.G.nodes(): #遍历每一个节点，找最近的节点
                    if single_node == node_id: #避免计算相同节点，形同节点距离是0，无法连边，没意义
                        continue
                    if self.G._node[single_node]["label"] == self.G._node[node_id]["label"]:
                        node_pair = [] #存放单节点和图中某一节点的节点对
                        dist = []  #计算单节点和当前图中某一个节点的相似度
                        node_pair.append(single_node)
                        node_pair.append(node_id)
                        dist.append(node_pair)
                        v2, v1 = np.array(self.train_data[int(node_id)]), np.array(self.train_data[int(single_node)])
                        d = np.linalg.norm(v2 - v1)
                        dist.append(d)
                        all_dist.append(dist)
                l = [a[1] for a in all_dist]  #将所有节点对的距离找出来
                index = l.index(min(l))    #找到最小节点对的索引
                #已经添加过节点了，所以不用再次添加节点，只需要连边就行了
                self.G.add_edge(all_dist[index][0][0], all_dist[index][0][1], weight=all_dist[index][1])

        #steps2: 小组件合并
        num = nx.number_connected_components(self.G)
        Gcc = sorted(nx.connected_components(self.G), key=len, reverse=True)
        #print(Gcc)
        for i in range(len(Gcc)): #循环每一个子图中
            two_pars_min = [] #存储两部分中所有最近的两个节点标签和距离
            for n in Gcc[i]:  #不影响使用，循环像影子图中的节点
                one_all_min = []
                count = 0  # 循环当前节点集合，然后跳出
                for x in range(i+1, len(Gcc)): #防止重复循环，所以从未计算过的子图节点开始计算

                    if self.G._node[list(Gcc[i])[0]]["label"] == self.G._node[list(Gcc[x])[0]]["label"]:
                        one_all_dist = []
                        for m in Gcc[x]:
                            #print("n, m:", n, m)
                            node_pair = []  # 存放单节点和图中某一节点的节点对
                            dist = []  # 计算单节点和当前图中某一个节点的相似度
                            node_pair.append(n)
                            node_pair.append(m)
                            dist.append(node_pair)
                            v2, v1 = np.array(self.train_data[int(m)]), np.array(self.train_data[int(n)])
                            d = np.linalg.norm(v2 - v1)
                            dist.append(d)
                            one_all_dist.append(dist)
                        #print("=="*20)
                        if one_all_dist:  #如果是labela不一样，那么就没有距离，one_all_dist就会是空，
                            l = [m[1] for m in one_all_dist]  # 将所有节点对的距离找出来
                            index = l.index(min(l))
                            min_dist = one_all_dist[index]
                            one_all_min.append(min_dist)
                            two_pars_min.append(one_all_min[0]) #只将元素添加进来就行了所以one_all_min[0],取其元素
                        count += 1
                    if count == 1:
                        break

                if two_pars_min: #如果找不到同类，就下一个节点集合，所以需要判断，
                    s = [m[1] for m in two_pars_min]
                    #print("s:", s)
                    index = s.index(min(s))
                    min_dist = two_pars_min[index]
                    #print("min_dist:", min_dist)
                    self.G.add_edge(min_dist[0][0], min_dist[0][1], weight=min_dist[1])

        return self.G

    def predict(self, test_data, test_target):
        """

        :param X_items: one node inserted
        :param nodeindex: the index of the inserted node
        :param Y_items: label of the inserted node
        :return:
        """
        self.X_test = test_data
        self.Y_test = test_target
        # 添加节点

        count = len(list(self.G.nodes()))
        for index, instance in enumerate(self.X_test):
            label = self.Y_test[index]
            # print("or_label:", label)
            # 计算插入节点之前的各个类别网络的measures
            # self.G0, self.G1 = self.get_subgraph(self.G)   #此时计算的是初始网络的measures，所以没必要重新计算节点的measures
            # measures0 = self.calculate_measure(self.G0)
            # measures0 = self.init_net_measure(self.G0)
            # self.net0_measure.append(measures0)
            # measures1 = self.calculate_measure(self.G1)
            # measures1 = self.init_net_measure(self.G1)
            # self.net1_measure.append(measures1)

            # 插入新的节点构建连边
            insert_node_id = count
            count += 1
            #print("insert_node_id:", insert_node_id)
            self.G.add_node(str(insert_node_id), values=instance, typeNode='test', label=label)
            radius_distances, radius_indices = self.epsilon_radius(self.nbrs[0], [instance],
                                                                   self.radius[0])
            distances, indices = self.KNN(self.nbrs[0], [instance])

            # 添加到训练网络中
            if (len(radius_indices)) > self.k:  # 判断用哪种方法连边构图,因为,radius应用于稠密区域，邻居大于k的话就是稠密
                for indiceNode, indicesNode in enumerate(radius_indices):
                    for tmpi, indice in enumerate(indicesNode):
                        if (str(indice) == str(indiceNode)):
                            continue
                        self.G.add_edge(str(indice), str(insert_node_id), weight=radius_distances[indiceNode][tmpi])
            else:
                for indiceNode, indicesNode in enumerate(indices):
                    for tmpi, indice in enumerate(indicesNode):
                        if (str(indice) == str(indiceNode)):
                            continue
                        self.G.add_edge(str(indice), str(insert_node_id), weight=distances[indiceNode][tmpi])

            self.classification(insert_node_id, int(self.Y_test[index]))
            #分类后删除节点
            if self.G.has_node(str(insert_node_id)):
                self.G.remove_node(str(insert_node_id))

    def classification(self, insert_node_id, label):
        # 因为在构建离岸边的时候用的就是str()形式，所以需要此处需要转化为字符串

        adj = [n for n in self.G.neighbors(str(insert_node_id))]  # find the neighbors of the new node
        # print("adj:", adj)
        # check which class the link of the new node belongs to
        count0 = 0
        count1 = 0
        for n in adj:
            if n in self.G0.nodes():
                label = self.G._node[n]["label"]
                # print("pre_label:", label)
                count0 += 1
            elif n in self.G1.nodes():
                label = self.G._node[n]["label"]
                # print("pre_label:", label)
                count1 += 1

        #print("edges_num:", count0, count1)
        if count0 == len(adj):
            self.predict_label.append(0)

        elif count1 == len(adj):

            self.predict_label.append(1)

        else:
            # print("模糊分类情况：")
            # self.draw_graph(self.G)

            dist_list = []
            if self.G.has_node(str(insert_node_id)):
                # print("Test node is in the init networks...................")
                self.G.remove_node(str(insert_node_id))

            # if not self.G.has_node(str(insert_node_id)):
                # print("Test node is not in the init networks...................")

            node_list0 = self.G0.nodes()  # 这时候还是插入节点之前的G0
            neighbor0 = [x for x in node_list0 if x in adj]

            node_list1 = self.G1.nodes()
            neighbor1 = [x for x in node_list1 if x in adj]

            if count0 >= 0 and count0 < len(adj):
                # 找到类1中和adj中相同的节点，然后将节点添加到类1中
                # node_list = self.G0.nodes()  # 这时候还是插入节点之前的G0
                # neighbor = [x for x in node_list if x in adj]
                # 然后将节点添加到类0中
                for n in neighbor0:
                    self.G.add_node(str(insert_node_id), typeNode='test', label=label)
                    self.G.add_edge(str(insert_node_id), n)
                # get the new sungraph to calclulate the measures
                self.G0, self.G1 = self.get_subgraph(self.G)

                # self.draw_graph(self.G0)
                # self.draw_graph(self.G1)

                measures0 = self.calculate_measure(self.G0)  # new subgraph self.G0 measures
                # 此处求得的可通信性的值接近原始网络的一半，误差会变小，所以此处不用求一半d
                # 最大值归一化
                # print(self.measures0, measures0)
                nor_measures0 = self.measures0
                nor_measures0, measures0 = self.max_normalization(nor_measures0, measures0)
                V1, V2 = np.array(nor_measures0), np.array(measures0)
                # print("v1, v2:", V1, V2)
                euclidean_dist0 = np.linalg.norm(V2 - V1)
                dist_list.append(euclidean_dist0)
                self.G.remove_node(str(insert_node_id))

            if count1 >= 0 and count1 < len(adj):
                #if str(insert_node_id) in self.G.nodes():
                    #self.G.remove_node(str(insert_node_id))
                # 找到类1中和adj中相同的节点，
                # node_list = self.G1.nodes()
                # neighbor = [x for x in node_list if x in adj]
                # 然后将节点添加到类1中
                for n in neighbor1:
                    self.G.add_node(str(insert_node_id), typeNode='test', label=label)
                    self.G.add_edge(str(insert_node_id), n)
                self.G0, self.G1 = self.get_subgraph(self.G)

                # self.draw_graph(self.G0)
                # self.draw_graph(self.G1)


                measures1 = self.calculate_measure(self.G1)
                # print(self.measures1, measures1)
                nor_measures1 = self.measures1
                nor_measures1, measures1 = self.max_normalization(nor_measures1, measures1)
                N1, N2 = np.array(nor_measures1), np.array(measures1)
                # print("N1, N2:", N1, N2)
                euclidean_dist1 = np.linalg.norm(N2 - N1)

                dist_list.append(euclidean_dist1)
                self.G.remove_node(str(insert_node_id))
            # 确定模糊分类节点的分类标签后，需要将节点移除，然后重新插入到确定的分类标签处
            # print(np.array(self.net0_measure), self.net1_measure, self.net2_measure,)
            # print("dist_list:", dist_list)
            # get the classfication ruselt
            # list = []
            # for x in dist_list:
            #     if not x == 0:
            #         list.append(x)
            if not sum(dist_list) == 0:
                # min_value = min(list)
                # label = int(dist_list.index(min_value))
                label = dist_list.index(min(dist_list))
                # print("classification_label:", label)
                #记录需要分类的节点
                self.need_classification.append(insert_node_id)
                self.predict_label.append(label)
            else:
                l = []
                l.extend((len(neighbor0), len(neighbor1)))
                # min_value = min(list)
                label = l.index(min(l))
                # label = int(dist_list.index(min_value))
                # print("classification_label:", label)
                # 记录需要分类的节点
                self.need_classification.append(insert_node_id)
                self.predict_label.append(label)
            # 因为是测试集，测试完不可能直接在放到训练集中，这是不对的
            """
            if label == 0:
                node_list = self.G0.nodes()
                neighbor = [x for x in node_list if x in adj]
                # 然后将节点添加到类1中
                self.G.add_node(str(insert_node_id), typeNode='test', label=label)
                for n in neighbor:
                    self.G.add_edge(str(insert_node_id), n)  # add edges

            if label == 1:
                node_list = self.G1.nodes()
                neighbor = [x for x in node_list if x in adj]
                # 然后将节点添加到类1中
                self.G.add_node(str(insert_node_id), typeNode='test', label=label)
                for n in neighbor:
                    self.G.add_edge(str(insert_node_id), n)
            """

    def score(self):
        label = list(map(int, self.Y_test))
        # print("original_label:", label)
        # print("predict_label :", self.predict_label)

        count = 0
        for i in range(len(self.Y_test)):
            if self.Y_test[i] == self.predict_label[i]:
                count += 1
        # print("正确个数：", count)
        accuracy = round(count / len(self.Y_test), 3)
        print("accuracy:", accuracy)
        print("need_classification:", self.need_classification)

        return accuracy






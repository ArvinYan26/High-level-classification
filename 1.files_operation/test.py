import random
from collections import Counter
# list0 = [20, 16, 10, 5]
# list1 = [21, 61, 11, 5]
# random.shuffle(list0)
# random.shuffle(list1)
# print("new_list:", list0)
# print("new_list:", list1)
#
#
# #random.shuffle(list)
#
#
#
# # a, b, c, d = 1, 2, 3, 4
# # c = []
# # c.extend(a, b, c, d)
# # print(c)
#
# s, l, = "one", "six"
# x = "one"
# if s == x:
#     print("hello")
# else:
#     print("wrong")
#
classs = ["head", "clothes", "shooes"]
classs_img = {"head":0, "clothes":0, "shooes":0}
pro_num = {"head":0, "clothes":0, "shooes":0}
name = [["head", "clothes", "shooes", "head", "head", "shooes"], ["head", "head", "head", "clothes", "shooes", "head", "head", "shooes"]]
# name1 = ["head", "head", "head", "clothes", "shooes", "head", "head", "shooes"]

# cal_img = Counter(list(set(name)))
# result = Counter(name)
#
# print(type(cal_img), cal_img)
# print(type(result), result)

# for name_i in classs:
#     if name_i in cal_img.keys():
for ele in name:
    print(type(ele))
    cal_img = Counter(list(set(ele)))
    result = Counter(ele)
    for key_name in cal_img.keys():
        classs_img[key_name] += cal_img[key_name]
        pro_num[key_name] += result[key_name]

        print("classs_img,pro_num", classs_img, pro_num)









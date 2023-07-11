import numpy as np

"""
34次high level 方法运行结果平均值
"""
# l = [0.9333, 0.6667, 0.7667, 0.8333, 0.7667, 0.8333, 0.8333, 0.8000, 0.7333, 0.9000]

l = [96.67, 96.67, 96.67, 96.67, 96.67, 90.00, 96.67, 96.67, 100.00, 100.00]
decimal_list = []

for percentage in l:
    decimal = round(percentage / 100, 4)
    decimal_list.append(decimal)

print(f"all_acc:{decimal_list}")
print(f"len:{len(decimal_list)}")
# acc = np.mean(l)
# x = round(acc, 4)
print(f"Average_acc:{np.mean(decimal_list):.4f}, Std:{np.std(decimal_list):.4f}")
#mena=0.96967
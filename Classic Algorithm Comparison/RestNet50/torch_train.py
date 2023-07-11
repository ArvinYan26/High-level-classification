import numpy as np
import torch
from torchvision import transforms, datasets
import torchvision.models as models
from torch.utils.data import DataLoader
import random
import time

# 定义数据集路径和其他参数
data_path = r"E:\Datasets\covid-19\COVID-19-c\sclect_datasets"  # 数据集路径
num_epochs = 40  # 训练轮数
batch_size = 20  # 批量大小
# 都是每个类别的大小，
train_size, test_size = 135, 15


# 设置随机种子以确保结果的可重复性
random.seed(0)


start_time = time.time()
# 数据预处理和增强
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # 调整图像大小为224x224
    transforms.ToTensor(),  # 转换为张量
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  # 标准化
])

# 加载数据集
dataset = datasets.ImageFolder(root=data_path, transform=transform)

# 获取每个类别的样本索引
class_indices = dataset.class_to_idx

print("class_indices:", class_indices)

indices = {c: [] for c in class_indices.keys()}

print("indices:", indices)

for i in range(len(dataset)):
    _, label = dataset[i]
    class_name = dataset.classes[label]
    indices[class_name].append(i)

# 随机选择训练集样本
train_indices = []
for idx in indices.values():
    train_indices.extend(random.sample(idx, train_size))

# 随机选择测试集样本
test_indices = []
for idx in indices.values():
    remaining_idx = set(idx) - set(train_indices)
    # test_indices.extend(random.sample(remaining_idx, test_size))
    test_indices.extend(random.choices(list(remaining_idx), k=test_size))
# 根据抽样结果获取训练集和测试集
train_dataset = torch.utils.data.Subset(dataset, train_indices)
# print("train_dataset:", len(train_dataset))
test_dataset = torch.utils.data.Subset(dataset, test_indices)
# print("test_dataset:", len(test_dataset))

print("train_data:{}, test_data:{}, epoch:{}".format(len(train_dataset), len(test_dataset), num_epochs))

# 存储每个模型的准确率和模型路径
accuracies = []
model_paths = []

# start_time = time()
# 训练多个模型
for i in range(10):
    # 创建数据加载器
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    # 创建并将模型移至GPU
    # model = models.resnet50(pretrained=True)    #下载预训练的模型，这个模型是在imagenet上训练过的，可能不适用于现在的模型，
    model = models.resnet50()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

    for epoch in range(num_epochs):
        # 训练模型
        model.train()
        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

    # 在测试集上评估模型
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total
    accuracies.append(accuracy)
    print(f"Model {i+1} Accuracy: {accuracy:.2f}%")
    print(f"accurance:{accuracy:.2f}")

    # 保存模型
    # model_path = f"model_{i+1}.pt"
    # torch.save(model.state_dict(), model_path)
    # model_paths.append(model_path)
all_acc = []
for percentage in accuracies:
    decimal = round(percentage / 100, 4)
    all_acc.append(decimal)


print(f"all_acc:{all_acc}")
print(f"len:{len(all_acc)}")
# acc = np.mean(l)
# x = round(acc, 4)
print(f"Average_acc:{np.mean(all_acc):.4f}, Std:{np.std(all_acc):.4f}")
# 计算平均准确率
# average_accuracy = sum(accuracies) / len(accuracies)

# std = np.std(accuracies)
# print(f"Average Accuracy: {average_accuracy:.2f}%, std:{std:.2f}", )

# 打印模型路径
# print("Model Paths:")
# for path in model_paths:
#     print(path)

import tensorflow as tf
import os

import torch

# 检查CUDA是否可用
print(torch.cuda.is_available())

# 获取当前使用的设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

# 打印CUDA设备数量
print(torch.cuda.device_count())


"""
# 检测GPU设备是否可用
print("GPU可用数量：", len(tf.config.experimental.list_physical_devices('GPU')))

# 检测TensorFlow是否使用了GPU
print("TensorFlow使用的设备：", tf.config.list_physical_devices('GPU'))

# 检测TensorFlow是否开启了GPU加速
print("TensorFlow是否开启了GPU加速：", tf.test.is_built_with_cuda())

# 检测GPU是否启用了内存增长
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print("GPU内存增长已启用")
    except RuntimeError as e:
        print(e)

model_name = "RestNet50_" + str(10) + ".h5"
path_save = "Classic Algorithm Comparison/RestNet50/model"
path = os.path.join(path_save, model_name)

print(path)

"""
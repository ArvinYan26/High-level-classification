import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# 设置测试数据集的路径
test_data_dir = r'E:\Datasets\covid-19\COVID-19\100\test'

# 加载训练好的模型
model = load_model('model/sieze_224_100/ResNet50_224_20.h5')

# 使用ImageDataGenerator加载和预处理测试数据
test_datagen = ImageDataGenerator(rescale=1./255)

test_generator = test_datagen.flow_from_directory(
    test_data_dir,
    target_size=(224, 224),
    batch_size=1,
    class_mode='categorical',
    shuffle=False)

# 评估模型在测试数据上的性能
test_loss, test_accuracy = model.evaluate(test_generator)
print('Test Loss:', test_loss)
print('Test Accuracy:', test_accuracy)

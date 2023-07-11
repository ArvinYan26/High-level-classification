import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import matplotlib.pyplot as plt

# 设置训练和验证数据集的路径
train_data_dir = r'E:\Datasets\covid-19\COVID-19\300\train'
valid_data_dir = r'E:\Datasets\covid-19\COVID-19\300\valid'

# 设置训练参数
batch_size = 8
epochs = 30
initial_learning_rate = 0.001
image_size = 1024

# 配置GPU设备
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        print(e)

# 加载预训练的ResNet50模型（不包括顶层）
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(image_size, image_size, 3))

# 冻结模型的权重，只训练自定义的顶层
for layer in base_model.layers:
    layer.trainable = False

# 添加自定义的顶层
model = tf.keras.models.Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(2, activation='softmax')
])

# 编译模型
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=initial_learning_rate),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# 使用ImageDataGenerator加载和预处理训练数据，并添加数据增强
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest')

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(1024, 1024),
    batch_size=batch_size,
    class_mode='categorical')

# 使用ImageDataGenerator加载和预处理验证数据
valid_datagen = ImageDataGenerator(rescale=1./255)

valid_generator = valid_datagen.flow_from_directory(
    valid_data_dir,
    target_size=(image_size, image_size),
    batch_size=batch_size,
    class_mode='categorical')

# 训练模型
# model.fit(train_generator,
#           epochs=epochs,
#           validation_data=valid_generator)


# 定义学习率衰减策略
lr_scheduler = tf.keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=3)

# 训练模型，并记录训练历史
history = model.fit(train_generator,
                    epochs=epochs,
                    callbacks=[lr_scheduler],
                    validation_data=valid_generator)  # 添加验证数据

# 绘制训练曲线
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Training Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend(['train', 'val'], loc='upper left')

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Training Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend(['train', 'val'], loc='upper left')

plt.tight_layout()
plt.show()


acc_image_name = "RestNet50_" + str(epochs) + ".jpg"
path_save = "model"
image_path = os.path.join(path_save, acc_image_name)
# 保存图表为 JPEG 文件，并指定图像质量
plt.savefig(image_path, dpi=300, quality=100)


model_name = "RestNet50_" + str(epochs) + ".h5"
path_save = "model"
path = os.path.join(path_save, model_name)
# 保存模型
model.save(path)




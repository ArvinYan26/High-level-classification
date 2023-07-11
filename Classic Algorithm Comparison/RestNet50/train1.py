import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

# 设置训练参数和相关配置
train_data_dir = r'E:\Datasets\covid-19\COVID-19\300\train'
valid_data_dir = r'E:\Datasets\covid-19\COVID-19\300\valid'

img_width, img_height = 224, 224
batch_size = 16
epochs = 30
initial_learning_rate = 0.001

# 检查GPU可用性
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)

# 构建模型
base_model = ResNet50(include_top=False, weights="imagenet", input_shape=(img_width, img_height, 3))

for layer in base_model.layers:
    layer.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
predictions = Dense(2, activation="softmax")(x)
model = Model(inputs=base_model.input, outputs=predictions)

# 模型编译
optimizer = Adam(learning_rate=initial_learning_rate)
model.compile(optimizer=optimizer, loss="categorical_crossentropy", metrics=["accuracy"])

# 数据生成器
train_datagen = ImageDataGenerator(rescale=1.0 / 255.0)
train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode="categorical"
)

# 使用ImageDataGenerator加载和预处理验证数据
valid_datagen = ImageDataGenerator(rescale=1./255)

valid_generator = valid_datagen.flow_from_directory(
    valid_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')


# 定义学习率衰减
def lr_decay(epoch):
    return initial_learning_rate * 0.9 ** epoch

lr_scheduler = tf.keras.callbacks.LearningRateScheduler(lr_decay)

# 定义模型检查点
checkpoint = tf.keras.callbacks.ModelCheckpoint("model_checkpoint.h5", save_best_only=True)

# 训练模型
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=epochs,
    callbacks=[lr_scheduler, checkpoint],
    validation_data=valid_generator
)

# 保存模型
model_name = "model/sieze_224_300/ResNet50_224_" + str(epochs) + ".h5"
model.save(model_name)
print("Model saved successfully.")

# 绘制准确率和损失曲线
plt.figure(figsize=(10, 5))

# 绘制准确率曲线
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

# 绘制损失曲线
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
name = "model/size_224_300/ResNet50_224_" + str(epochs) + ".png"
plt.savefig(name)
plt.show()

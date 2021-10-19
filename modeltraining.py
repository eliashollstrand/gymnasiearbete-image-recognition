import tensorflow as tf

import os
import numpy as np
import matplotlib.pyplot as plt

base_dir = "/Users/Elev/Documents/Tensorflow Face Recognition/images/train"

IMAGE_SIZE = 224

BATCH_SIZE = 4

data_generator = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1. / 255,
    validation_split=0.2)

train_generator = data_generator.flow_from_directory(
    base_dir,
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE,
    subset='training')

val_generator = data_generator.flow_from_directory(
    base_dir,
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE,
    subset='validation')

for image_batch, label_batch in train_generator:
    break

print(train_generator.class_indices)

labels = '\n'.join(sorted(train_generator.class_indices.keys()))

with open('labels.txt', 'w') as f:
    f.write(labels)

IMG_SHAPE = (IMAGE_SIZE, IMAGE_SIZE, 3)

base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights='imagenet')

base_model.trainable = False

model = tf.keras.Sequential([
    base_model,  
    tf.keras.layers.Conv2D(32, 3, activation='relu'),  
    tf.keras.layers.Dropout(0.2),  
    tf.keras.layers.GlobalAveragePooling2D(),  
    tf.keras.layers.Dense(3, activation='softmax')  
])

model.compile(optimizer=tf.keras.optimizers.Adam(),  
              loss='categorical_crossentropy',  
              metrics=['accuracy'])  

model.summary()

print('Number of trainable variables = {}'.format(len(model.trainable_variables)))

epochs = 10

history = model.fit(train_generator,
                    epochs=epochs,
                    validation_data=val_generator)

base_model.trainable = True

print("Number of layers in the base model: ", len(base_model.layers))

fine_tune_at = 100

for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

model.compile(loss='categorical_crossentropy',
              optimizer=tf.keras.optimizers.Adam(1e-5),
              metrics=['accuracy'])

model.summary()

print('Number of trainable variables = {}'.format(len(model.trainable_variables)))

history_fine = model.fit(train_generator,
                         epochs=5,
                         validation_data=val_generator
                         )


saved_model_dir = 'saved model/fine_tuning.h5'
model.save(saved_model_dir)
print("Model Saved to saved model/fine_tuning.h5")
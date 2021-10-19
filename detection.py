import tensorflow as tf
from tensorflow.keras.applications.mobilenet import preprocess_input
from tensorflow.keras.preprocessing import image
import numpy as np
from matplotlib import pyplot as plt

# Image of Elias
# img = "images/test/Elias.b195b325-211b-11ec-81af-84fdd18c7552.jpg"

# Image of Jeff Bezos
img = "images/test/jeff.jpg"

img = image.load_img(img, target_size=(224, 224))

img_array = image.img_to_array(img)
img_batch = np.expand_dims(img_array, axis=0)

img_preprocessed = preprocess_input(img_batch)

model = tf.keras.models.load_model('saved model/fine_tuning.h5')
model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

prediction = model.predict(img_preprocessed)
print(prediction)

classes = np.argmax(prediction, axis = 1)
detected_class_index = classes[0]

labels = open("labels.txt", 'r')

for position, line in enumerate(labels):
    if position == detected_class_index:
        print("Detected: " + line)


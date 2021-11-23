import numpy as np
import io
import os
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from PIL import Image, ImageDraw, ImageFont, ImageOps
from datetime import datetime
from googleapiclient.http import MediaIoBaseDownload
from Google import Create_Service #Google.py source code: https://learndataanalysis.org/google-drive-api-in-python-getting-started-lesson-1/
 
now = datetime.now()
time = now.strftime("%Y-%m-%d %H.%M.%S")
print("Recieved at " + time)

img_height, img_width = 250, 250
class_names = ['Elias', 'Vincent']
num_classes = len(class_names)

CLIENT_SECRET_FILE = 'client_secrets.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

test_path = ""

def detect(obj):
    
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES) 
    results = service.files().list(fields="nextPageToken, files(id, name, mimeType, size, parents)").execute()
    items = results.get('files', [])

    for item in items:
        if(item["id"] == obj["id"]):
            request = service.files().get_media(fileId=item["id"])
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print ("Download %d%%." % int(status.progress() * 100))

            fh.seek(0)

            with open(os.path.join("undetected_images/", item["name"]), "wb") as file:
                file.write(fh.read())
                file.close
                test_path = "undetected_images/" + item["name"]

    # #Elias
    # # test_path = 'datasets/face_dataset_test_images/Elias/elias10.jpg'

    # #Vincent
    # # test_path = 'datasets/face_dataset_test_images/Vincent/vincent2.jpg'

    test_image = image.load_img(test_path, target_size=(img_height, img_width, 3))
    test_image = image.img_to_array(test_image)  # from image to array
    # shape from (250, 250, 3) to (1, 250, 250, 3)
    test_image = np.expand_dims(test_image, axis=0)

    model_name = 'face_classifier.h5'
    model = keras.models.load_model(f'models/{model_name}')

    result = model.predict(test_image)

    classes = np.argmax(result, axis = 1)
    # detected_class_index = classes[0]
    confidence_percent = str(round(max(result[0])*100, 2))

    detected_class = ""
    predictions = []
    for index in range(num_classes):
        print("{:6} with probabily of {:.2f}%".format(class_names[index], result[0][index] * 100))
        predictions.append(result[0][index] * 100)

    for i in range(len(predictions)):
        if(predictions[i] == max(predictions)):
            detected_class = class_names[i]

    print("=> Detected: " + detected_class)
            
    # Save image with detected class label text
    result_image = Image.open(test_path)
    result_image = ImageOps.exif_transpose(result_image) # Prevents image from rotating if it has an EXIF orientation tag
    image_editable = ImageDraw.Draw(result_image)
    class_text = str(detected_class + ": " + confidence_percent + "%")
    W, H = result_image.size
    text_font = ImageFont.truetype('C:\\Users\\Elev\\AppData\\Local\\Microsoft\\Windows\\Fonts\\Rubik-Regular.ttf', round(W*0.05))
    w, h = image_editable.textsize(class_text, font=text_font)

    # Text color is set to red if the prediction confidence is lower than or equal to 50%
    # Otherwise green
    text_color = ""
    if(float(confidence_percent) >= 50):
        text_color = (19, 252, 3)
    else:
        text_color = fill='red'

    image_editable.text(((W-w)/2, 20), class_text, text_color, font=text_font)

    result_image.save("detected_images/" + time + ".jpg")
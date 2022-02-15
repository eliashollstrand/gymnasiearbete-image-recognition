import numpy as np
import io
import os
import cv2
import shutil
import tensorflow as tf
from PIL import Image, ImageDraw, ImageFont, ImageOps
from datetime import datetime
from googleapiclient.http import MediaIoBaseDownload
from Google import Create_Service #Google.py source code: https://learndataanalysis.org/google-drive-api-in-python-getting-started-lesson-1/
from preprocess import preprocess
from layers import L1Dist
from img_processing import crop_to_face

model_name = 'siamesemodel_v4.h5' # The model to be used

CLIENT_SECRET_FILE = 'client_secrets.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

def save_image(v, path, time):
    if(v):
        detected = 'Elias'
    else:
        detected = 'Unknown'

    print("\n=> Detected: " + detected)
            
    # Save image with detected class label text
    result_image = Image.open(path)
    result_image = ImageOps.exif_transpose(result_image) # Prevents image from rotating if it has an EXIF orientation tag
    image_editable = ImageDraw.Draw(result_image)
    W, H = result_image.size
    text_font = ImageFont.truetype('C:\\Users\\Elev\\AppData\\Local\\Microsoft\\Windows\\Fonts\\Rubik-Regular.ttf', round(W*0.05))

    text_color = ""
    if(v):
        class_text = str(detected)
        text_color = (19, 252, 3)
    else:
        class_text = "Unknown"
        text_color = 'red'

    w, h = image_editable.textsize(class_text, font=text_font)
    image_editable.text(((W-w)/2, 20), class_text, text_color, font=text_font)

    result_image.save("application_data/detected_images/" + time + " - " + detected + ".png")

def verify(model, detection_threshold, verification_threshold, path):
    # Build results array
    results = []
    for image in os.listdir(os.path.join('application_data', 'verification_images')):
        input_img = preprocess(os.path.join(path))
        validation_img = preprocess(os.path.join('application_data', 'verification_images', image))
        
        # Make Predictions 
        result = model.predict(list(np.expand_dims([input_img, validation_img], axis=1)))
        results.append(result)
    
    # Detection Threshold: Metric above which a prediciton is considered positive 
    detection = np.sum(np.array(results) > detection_threshold)
    
    
    # Verification Threshold: Proportion of positive predictions / total positive samples 
    verification = detection / len(os.listdir(os.path.join('application_data', 'verification_images'))) 
    print(f"Threshold is: {verification_threshold}")
    print(f"Verification is: {verification}")
    verified = verification > verification_threshold
    return verified

def detect(obj):
    now = datetime.now()
    time = now.strftime("%Y-%m-%d %H.%M.%S")
    
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

            with open(os.path.join("application_data/input_image/", item["name"]), "wb") as file:
                file.write(fh.read())
                file.close

                image_path = "application_data/input_image/" + item["name"]
                app_image_path = image_path.replace("input_image", "display_images")
                
                crop_to_face(image_path)
                
                model = tf.keras.models.load_model(f"models/{model_name}", 
                                   custom_objects={'L1Dist':L1Dist, 'BinaryCrossentropy':tf.losses.BinaryCrossentropy})
                
                detected = verify(model, 0.5, 0.5, image_path)
                print("\nVerification returned " + str(detected))
                save_image(detected, app_image_path, time)
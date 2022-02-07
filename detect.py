import numpy as np
import io
import os
import cv2
import tensorflow as tf
from PIL import Image, ImageDraw, ImageFont, ImageOps
from datetime import datetime
from googleapiclient.http import MediaIoBaseDownload
from Google import Create_Service #Google.py source code: https://learndataanalysis.org/google-drive-api-in-python-getting-started-lesson-1/
from preprocess import preprocess
from layers import L1Dist

model_name = 'siamesemodel.h5' # The model to be used

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
    verified = verification > verification_threshold
    return verified

def crop_to_face(path):
    img = cv2.imread(path)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
    
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    # Draw rectangle around the faces and crop the faces
    for (x, y, w, h) in faces:
        dx = 0
        dy = 0
        if(y-100 < 0):
            Y = 0
            dy = abs(y-100)
        else:
            Y = y-100
        if(x-100 < 0):
            X = 0
            dx = abs(x-100)
        else:
            X = x-100
        faces = img[Y:y + h + dy + 100, X:x + w + dx + 100] 

    cv2.imwrite(path, faces)
    return path

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
                image_path = crop_to_face(image_path)
                model = tf.keras.models.load_model(model_name, 
                                   custom_objects={'L1Dist':L1Dist, 'BinaryCrossentropy':tf.losses.BinaryCrossentropy})
                detected = verify(model, 0.5, 0.5, image_path)
                print("\nVerification returned " + str(detected))
                save_image(detected, image_path, time)
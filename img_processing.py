import cv2
from cvzone.SelfiSegmentationModule import SelfiSegmentation

def crop_to_face(path):
    print(path)
    img = cv2.imread(path)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_alt2.xml')
    
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    for (x, y, w, h) in faces:
        faces = img[y:y + h , x:x + w]

    try:
        cv2.imwrite(path, faces)
        cv2.imwrite(path.replace("input_image", "display_images"), img)
    except:
        print("Error")
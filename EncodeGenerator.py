import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

import io

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : "Add Your Database Cred here",
    'storageBucket' : "Add Your Storage Bucket Here"
})

# Define the desired image size
IMAGE_SIZE = (216, 216)

folderPath = 'Images'
PathList = os.listdir(folderPath)
imgList = []
studentIds = []
for path in PathList:
    # Read the original image from file
    img = cv2.imread(os.path.join(folderPath, path))
    imgList.append(img)
    studentIds.append(os.path.splitext(path)[0])

print(studentIds)

def findEncoding(imagesList):
    encodeList = []
    for img in imagesList:
        # Convert the original image from BGR to RGB format
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Encoding started...")
encodeListKnown = findEncoding(imgList)
# print(encodeListKnown)
encodeListKnownwithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownwithIds, file)
file.close()
print("File Saved")

# Resize and upload the images to Firebase storage
for i in range(len(PathList)):
    # Read the original image from file
    img = cv2.imread(os.path.join(folderPath, PathList[i]))
    # Resize the image
    resized_img = cv2.resize(img, IMAGE_SIZE)
    # Convert the resized image from BGR to RGB format
    resized_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)

    # Upload the resized image to Firebase storage in PNG format
    fileName = f'{folderPath}/{studentIds[i]}.png'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    # Encode the resized image to PNG format and upload it to the blob
    _, buffer = cv2.imencode('.png', resized_img)
    blob.upload_from_string(buffer.tobytes(), content_type='image/png')

print("Images resized and uploaded to Firebase storage.")


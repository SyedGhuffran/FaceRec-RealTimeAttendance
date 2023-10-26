# Standard library imports

import sys
import time
import csv
from datetime import datetime
import vlc
import tkinter as tk
from tkinter import messagebox

import os
from PIL import Image


# Third-party library imports
import dlib
import cvzone
import cv2
import numpy as np
import face_recognition
import firebase_admin
from firebase_admin import credentials, db, storage


import pickle

script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

# Set the environment variable to the script directory
os.environ["FACE_RECOGNITION_MODEL_PATH"] = script_directory

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : "Add Your Database Cred here",
    'storageBucket' : "Add Your Storage Bucket Here"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# importing images
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))


# importing the encodings
file = open('EncodeFile.p', 'rb')
encodeListKnownwithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownwithIds
print(studentIds)

modeType = 0
counter = 0
id = -1
imgStudent = []
foundQR = False
def play_beep():
    player = vlc.MediaPlayer("beep.wav")
    player.play()


while True:
    success, img = cap.read()




    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurrFrame = face_recognition.face_locations(imgS)
    encodeCurrFrame = face_recognition.face_encodings(imgS, faceCurrFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]


    for encodeFace, faceLoc in zip(encodeCurrFrame, faceCurrFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print("Distance ", faceDis)
        matchIndex = np.argmin(faceDis)
        print("Index No. ", np.argmin(faceDis))
        # print("Match Index ", matchIndex)
        # print("matches ", matches)
        # print("Distance ", faceDis)
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1

        if np.min(faceDis) < 0.5:
            print("Known Face Detected")
            print("The match is", studentIds[matchIndex])
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
            id = studentIds[matchIndex]
            studentsInfo = db.reference(f'Employees/{id}').get()
            print("Student's information is", studentsInfo)

            recognized_face_img = img[y1:y2, x1:x2]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = studentsInfo['name']
            file_path = f"Recognized/{name}_{timestamp}.png"
            cv2.imwrite(file_path, recognized_face_img)

            if counter == 0:
                counter = 1
                modeType = 1
                play_beep()
            if studentsInfo:
                with open('attendance.csv', mode='a', newline='') as csv_file:
                    fieldnames = ['ID', 'Name', 'Day', 'Month', 'Year', 'Hour']
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    now = datetime.now()
                    day = now.strftime("%d")
                    month = now.strftime("%m")
                    year = now.strftime("%Y")
                    hour = now.strftime("%H:%M:%S")
                    name = studentsInfo['name']
                    writer.writerow({'ID': id, 'Name': name, 'Day': day, 'Month': month, 'Year': year, 'Hour': hour})
        else:
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
            print("Unknown face detected")
            modeType = 4
            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
            unrecognized_face_img = img[y1:y2, x1:x2]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = f"Unrecognized/unrecognized_{timestamp}.png"
            cv2.imwrite(file_path, unrecognized_face_img)

    if counter != 0:
        if counter == 1:
            studentsInfo = db.reference(f'Employees/{id}').get()
            print(studentsInfo)
            blob = bucket.get_blob(f'Images/{id}.png')
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
        #try:
             #studentsInfo['total_attendance'] +=1
        #except:
            #ref.child('total_attendance').set(int(studentsInfo['total_attendance']))
        #continue
        #ref.child('total_attendance').set(studentsInfo['total_attendance'])

        if 5 < counter < 10:
            modeType = 2

        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

        if counter <= 5:
            # cv2.putText(imgBackground, str(studentsInfo['']), (861, 125),
            #             cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
            cv2.putText(imgBackground, str(studentsInfo['designation']), (1006, 550),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
            cv2.putText(imgBackground, str(id), (1006, 493),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
            #cv2.putText(imgBackground, str(studentsInfo['department']), (910, 625),
            #            cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)
            #cv2.putText(imgBackground, str(studentsInfo['department']), (1025, 625),
            #            cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)
            #cv2.putText(imgBackground, str(studentsInfo['work_location']), (1125, 625),
            #            cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)

            (w, h), _ = cv2.getTextSize(studentsInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
            offset = (414 - w) // 2
            cv2.putText(imgBackground, str(studentsInfo['name']), (808 + offset, 445),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)

            imgBackground[175:175 + 216, 909:909 + 216] = imgStudent
        counter += 1
        if 20 > counter >= 10:
            counter = 0
            modeType = 0
            studentsInfo = []
            imgStudent = []
            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]


    #cv2.imshow("Webcam", img)
    cv2.imshow("Face Recognition", imgBackground)
    cv2.waitKey(1)

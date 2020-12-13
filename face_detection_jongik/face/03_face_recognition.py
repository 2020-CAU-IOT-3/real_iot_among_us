"""
from threading import Thread
import time
import cv2
import numpy as np
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "/home/pi/face/cascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0
#미션 시작하기
def missionstarter():
    actflag = 0
    check = []

    global mate1flag
    global mate2flag
    global mate3flag
    mate1flag = 0
    mate2flag = 0
    mate3flag = 0

    while True:
        # 서버에서 미션 완료 데이터 받아오는 곳(
        if 미션 완료:
            actflag = 0

        #미션 시작 여부 결정
        if actflag == 0:
            if len(check) <= 50:
                if mate1flag == 1:
                    check.append(1)
                    mate1flag = 0
                elif mate2flag == 1:
                    check.append(2)
                    mate2flag = 0
                elif mate3flag == 1:
                    check.append(3)
                    mate3flag = 0
                else:
                    check.append(0)
            else:
                if mate1flag == 1:
                    check.append(1)
                    mate1flag = 0
                elif mate2flag == 1:
                    check.append(2)
                    mate2flag = 0
                elif mate3flag == 1:
                    check.append(3)
                    mate3flag = 0
                else:
                    check.append(0)
                check.pop(0)
            print(check)
        if check.count(1) == 30:
            actflag = 1
            print("missionstart") # 이부분 지우시고 서버로 미션 시작 신호 보내시면 됩니다.
        elif check.count(2) == 30:
            actflag = 1
            print("missionstart") # 이부분 지우시고 서버로 미션 시작 신호 보내시면 됩니다.
        elif check.count(3) == 30:
            actflag = 1
            print("missionstart") # 이부분 지우시고 서버로 미션 시작 신호 보내시면 됩니다.

        time.sleep(1/6)
    return

missionth = Thread(target=missionstarter)
missionth.start()
# names related to ids: example ==> loze: id=1,  etc
names = ['imposter', 'crewmate1', 'crewmate2', 'crewmate3']

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height
cam.set(cv2.CAP_PROP_FPS,15) # set video frame
# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

while True:
    ret, img =cam.read()
    img = cv2.flip(img, -1) # Flip vertically
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
    )

    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        # Check if confidence is less them 100 ==> "0" is perfect match
        if (confidence < 100):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
            if(id == "crewmate1"):
                mate1flag = 1

            if(id == "crewmate2"):
                mate2flag = 1

            if(id == "crewmate3"):
                mate3flag = 1
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))

        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)

    cv2.imshow('camera',img)
    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
"""
import cv2
import numpy as np
import os
import requests,json,threading,time

serverAddress = 'http://192.168.0.17:5000/missionCrewUpdate'
headers = {'Content-Type': 'application/json'}
room_number = 1


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer\\trainer.yml')
cascadePath = "cascades\\haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> loze: id=1,  etc
names = ['0', '1', '2', '3', '4']

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)
prev_id = 'None'
while True:
    ret, img =cam.read()
    #img = cv2.imread("C:\\Users\\yu990\\Desktop\\User.1.1.jpg")
    img = cv2.flip(img, 1) # Flip vertically
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )
    if len(faces) == 0:
        id = '0'
        #print("Face Not Found!")

    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        # Check if confidence is less them 100 ==> "0" is perfect match
        if (confidence < 100):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))

        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)

    cv2.imshow('camera', img)

    if prev_id != id:
        data = {'room': str(room_number), 'type': id}
        r = requests.post(serverAddress, headers=headers, data=json.dumps(data))
        print("now:"+r.text)
    prev_id = id
    cv2.imshow('camera',img)
    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()

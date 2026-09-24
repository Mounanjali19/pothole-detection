import cv2 as cv
import time
import requests
import subprocess as sp
from ultralytics import YOLO
from PIL import Image





i = 0


pothole_data = []
model = YOLO('best.pt')

try:
    cap = cv.VideoCapture('test.mp4')
    width = cap.get(3)
    height = cap.get(4)
    fourcc= cv.VideoWriter_fourcc(*'mp4v')
    out = cv.VideoWriter(f'output{i}.mp4',fourcc,30.0,(int(width),int(height)))

except Exception as e:
    print("error opening webcam")
    exit(1)

        
while True:
    ret, frame = cap.read()  
    if not ret:
        print("error reading frame")
        break
    try:
        results = model.track(frame, classes=0, conf=0.4, imgsz=480)
        cv.putText(frame,'', (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)
        cv.imshow("Live Camera", results[0].plot())
        names= results[0].names
        boxes = results[0].boxes.xyxy.cpu().numpy()
        scores=results[0].boxes.conf.cpu().numpy()
    except Exception as e:
        print(f"error detecting objects{e}")
        continue

    for(class_name,score,box) in zip(names,scores,boxes):
        label = "pothole"
        x,y,w,h = box
        box_area = w*h
        frame_area = width*height

        severity='low'
        if box_area/frame_area>0.1:
            severity="high"
        elif box_area/frame_area>0.02:
            severity='medium'


    
    key=cv.waitKey(1)
    if key==ord('q'):
        break

# End
out.release()
cap.release()
cv.destroyAllWindows()

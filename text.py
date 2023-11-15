import cv2
from cv2 import imread
import numpy as np
#source from https://github.com/ankit16-py/YOLOv3-KCF-Fast-Object-Tracker
#SEARCH_OBJECT = ('Hamburger','Macaron','Fries','Banana','Strawberry','meal bag','chicken nuggets','ICE cream','black tea','green tea','milk tea')
SEARCH_OBJECT = ['Hamburger','Macaron','Fries','Banana','Strawberry','meal bag','chicken nuggets','ICE cream','black tea','green tea','milk tea']
#SEARCH_OBJECT = {'Hamburger','Macaron','Fries','Banana','Strawberry','meal bag','chicken nuggets','ICE cream','black tea','green tea','milk tea'}
#SEARCH_OBJECT ='Macaron'
VIDEO = 'meal-bag-2429.jpg'
OBJ_THRESHOLD=0.5
CONF_THRESHOLD=0.5
NMS_THRESHOLD=0.5
WIDTH=500#540
HEIGHT=500#960
def process_and_draw(frame, out, timer):
    imghei = frame.shape[0]
    imgwid = frame.shape[1]
    classids = []
    confs = []
    boxes = []
    for o in out:
        for detected in o:
            if detected[4] > OBJ_THRESHOLD:
                #print (detected[4])
                scores = detected[5:]
                #print (scores)
                classid = np.argmax(scores)
                conf = scores[classid]
                #print (conf)
                for i in SEARCH_OBJECT:
                    if conf > CONF_THRESHOLD and classes[classid] == i:
                        food=i
                        center_x = int(detected[0] * imgwid)
                        center_y = int(detected[1] * imghei)
                        w = int(detected[2] * imgwid)
                        h = int(detected[3] * imghei)
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        classids.append(classid)
                        confs.append(float(conf))
                        boxes.append([x, y, w, h])
                        #print (boxes)
    ind = cv2.dnn.NMSBoxes(boxes, confs, CONF_THRESHOLD, NMS_THRESHOLD)
    conf = max(confs)
    for i in ind:
        box = boxes[i]
        print (box)
        cframe = frame.copy()
        draw_label(frame, box, timer,food+str(conf))

    if len(boxes) == 0:
        box = []
        food=None
        cframe = frame.copy()
    print (classid)
    f = open('movies.txt','w')
    print(classid, file = f)
    f.close()
    return box, cframe,food+str(conf)

#物件偵測
def object_detector(frame,model, timer):
    blob=cv2.dnn.blobFromImage(frame,1/255,(WIDTH,HEIGHT),[0,0,0],1,crop=False)
    model.setInput(blob)
    out=model.forward(model.getUnconnectedOutLayersNames())
    tbox,cframe,food=process_and_draw(frame,out, timer)
    return tbox,cframe,food

def draw_label(frame, box, timer,food=None):
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.putText(frame, "FPS : " + str(int(fps)), (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)
    cv2.putText(frame, "YOLO Detect", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)

    if box == None:
        cv2.putText(frame, "Tracking failure detected", (20,80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
    else:
        cv2.rectangle(frame, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (255, 255, 0), 3)
        cv2.putText(frame, food, (box[0], box[1]), cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 255, 0), 2)
    cv2.imshow('F',frame)

model=cv2.dnn.readNetFromDarknet('yolov4-tiny.cfg','yolov4-tiny_final.weights')
classes=None
with open('my_data.name','rt') as f:
    classes=f.read().rstrip('\n').split('\n')

cap = cv2.VideoCapture(VIDEO)

tflag=0

while(cap.isOpened()):
    ok,frame=cap.read()
    timer=cv2.getTickCount()
    if not ok:
        break
    
    tbox,cframe,food=object_detector(frame,model,timer)
    if len(tbox)==0 or food == None:
        draw_label(cframe, None, timer,None)
    else:
        draw_label(cframe, tbox, timer,food)

    k=cv2.waitKey(10000)
    if k==ord('q'):
        break
  
cap.release()
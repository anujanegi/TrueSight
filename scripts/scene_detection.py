import os
import argparse
import imutils

import cv2
import numpy as np
from time import time, sleep

from imutils.video import FPS
from imutils.video import VideoStream

from .scene_classification import scene_classification
from .sentence_classification import *
from .text_to_speech import *

def capture_frame():
    vs = VideoStream(src=1).start()
    # sleep(2.0)
    img = vs.read()
    # cv2.imshow('ss',img)
    return img

def scene_detect():
    # initialize the list of class labels MobileNet SSD was trained to
    # detect, then generate a set of bounding box colors for each class
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
        "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    # load our serialized model from disk
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe("./models/MobileNetSSD_deploy.prototxt.txt", "./models/MobileNetSSD_deploy.caffemodel")

    # initialize the video stream, allow the cammera sensor to warmup,
    # and initialize the FPS counter
    print("[INFO] starting video stream...")

    # =========================================
    # CHANGE src = 0 to src = 1 to use DroidCam
    # =========================================

    vs = VideoStream(src=1).start()
    sleep(2.0)
    fps = FPS().start()
    res = list()
    # Initialise variables to store current time difference as well as previous time call value
    previous = time()
    delta = 0
    gamma = 0
    # Capture Once only
    # Get the current time, increase delta and update the previous variable
    current = time()
    delta += current - previous
    gamma += current - previous
    previous = current

    # Check if 3 (or some other value) seconds passed

    # Show the image and keep streaming
    img = vs.read()
    scene = list()
    # if delta > 3:
    # Operations on image
    # Reset the time counter
    cv2.imwrite('DontCare.jpg', img)
    temp = scene_classification('DontCare.jpg')
    # if(list(set(scene))[0]!=temp):
    sent_scene = scene_sentence(temp)
    print(sent_scene)
    speech(sent_scene)
    delta = 0
    scene.append(temp)
    os.remove('DontCare.jpg')
    res.append(sent_scene)
        

    frame = vs.read()
    frame = imutils.resize(frame, width=600)

    # grab the frame dimensions and convert it to a blob
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
        0.007843, (300, 300), 127.5)

    # pass the blob through the network and obtain the detections and
    # predictions
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > 0.4:
            # extract the index of the class label from the
            # `detections`, then compute the (x, y)-coordinates of
            # the bounding box for the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # draw the prediction on the frame
            label = "{}: {:.2f}%".format(CLASSES[idx],
                confidence * 100)

            
            
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
            if(confidence>0.85):
                gamma = 0
                if(CLASSES[idx]=="person"):
                    '''
                    Ankur's code
                    '''
                    sent_person = known_face_sentence(CLASSES[idx])
                    # print(sent_person)
                    # speech(sent_person)
                    res.append(sent_person)
                else:
                    sent_obj = object_sentence(CLASSES[idx])
                    res.append(sent_obj)
                    # print(sent_obj)
                    # speech(sent_obj)
            else:
                res.append(None)
            
            return res


    # show the output frame
    # cv2.imshow("Frame", frame)
    # key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    # if key == ord("q"):
        # break

    # update the FPS counter
    # fps.update()

# stop the timer and display FPS information
# fps.stop()
# print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
# print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# # do a bit of cleanup
# cv2.destroyAllWindows()
# vs.stop()

if __name__ == '__main__':
    scene_detect()
import cv2
from text_detection import TextDetector

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 1)

while True:
    ret, frame = cap.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    data = TextDetector.detect(frame.copy())

    if data:
        print(data)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
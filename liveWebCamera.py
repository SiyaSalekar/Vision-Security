# install opencv required - pip install opencv-python
import cv2

# capture video
cap = cv2.VideoCapture(0)

# set frame
while cap.isOpened():
    ret, frame = cap.read()

    cv2.imshow('Webcam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
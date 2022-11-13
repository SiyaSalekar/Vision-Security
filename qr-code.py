import cv2
import RPi.GPIO as GPIO
import time

# set up the camera object
cap = cv2.VideoCapture(0)

# QR code detection object
detector = cv2.QRCodeDetector()

while True:
    # get the image
    _, img = cap.read()
    # fetch the bounding box co-ordinates and data
    data, bboxcord, _ = detector.detectAndDecode(img)

    # draw bounding box along with the data
    if (bboxcord is not None):

        cv2.putText(img, data, (int(bboxcord[0][0][0]), int(bboxcord[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
        if data:
            print("Found: ", data)

            # LED Setup
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(8, GPIO.OUT)

            # control LED when data received set output to HIGH
            for i in range(0,2):
                GPIO.output(8, True)
                time.sleep(0.5)
                GPIO.output(8, False)
                time.sleep(0.5)
            GPIO.cleanup()

    # Image preview
    cv2.imshow("Image", img)

    if (cv2.waitKey(1) == ord("q")):
        break

# free camera object and exit
cap.release()
cv2.destroyAllWindows()




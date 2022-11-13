import cv2

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

        cv2.putText(img, data, (tuple(bboxcord[0][0][0]), tuple(bboxcord[0][0][1]) - 10), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                    0.5, (0, 255, 0), 2)
        if data != None:
            print("Found: ", data)
    # Image preview
    cv2.imshow("Image", img)
    if (cv2.waitKey(1) == ord("q")):
        break
# free camera object and exit
cap.release()
cv2.destroyAllWindows()
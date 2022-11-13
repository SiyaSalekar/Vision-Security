import json
import cv2
from flask import Flask, render_template
import threading

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/qrcode")
def qrcode():
    global data
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
                if data:
                    print("Found: ", data)
                    return str(data)

        # Image preview
        cv2.imshow("Image", img)

        if (cv2.waitKey(1) == ord("q")):
            break

    # free camera object and exit
    cap.release()
    cv2.destroyAllWindows()




if __name__ == '__main__':
    #app.run(host='192.168.43.136',port=9000)
    sensors_thread = threading.Thread(target=qrcode)
    sensors_thread.start()
    app.run(debug=True)




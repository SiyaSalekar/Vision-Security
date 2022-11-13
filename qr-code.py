import json
import cv2
from flask import Flask, render_template
import threading

app = Flask(__name__)


# pubnub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'mySubscribeKey'
pnconfig.publish_key = 'myPublishKey'
pnconfig.user_id = "my_custom_user_id"
pubnub = PubNub(pnconfig)

def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];

class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pubnub.publish().channel('my_channel').message('Hello world!').pn_async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        # Handle new message stored in message.message
        print(message.message)

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('my_channel').execute()

# pubnub endRegion

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




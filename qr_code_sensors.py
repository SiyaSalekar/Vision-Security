import cv2
from flask import Flask, render_template, request, redirect, json
import mysql.connector
import RPi.GPIO as GPIO
import time

# pubnub imports
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

myChannel = 'siyas-channel'
sensorsList = ["led"]
# transmission PubNub
dataD = {}
# image
data = {}

pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-babca055-8ae8-4cbb-87e3-d1927bc7826a"
pnconfig.publish_key = "pub-c-7b7bf3ef-a5df-4ec8-9bb2-f70cc90f6c86"
pnconfig.user_id = "Jack-device"
pubnub = PubNub(pnconfig)

app = Flask(__name__)

# database connect
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Siya@123',
    database='vision_security'
)

# database connect endRegion


def publish(custom_channel, msg):
    pubnub.publish().channel(custom_channel).message(msg).pn_async(my_publish_callback)


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
            pubnub.publish().channel(myChannel).message('Connected to PubNub').pn_async(my_publish_callback)
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
        try:
            print(message.message)
            msg = message.message
            key = list(msg.keys())
            print(key)
            if key[0] == "event":  # {"event":{"sensor_name":True}}
                self.handleEvent(msg)
            if key[0] == "scan":
                self.qr_validate()
        except Exception as e:
            print("Received: ", message.message)
            print(e)
            pass

    def handleEvent(self, msg):
        global dataD
        eventData = msg["event"]
        key = list(eventData.keys())
        if key[0] in sensorsList:
            if eventData[key[0]] is True:
                dataD["alarm"] = True
            if eventData[key[0]] is False:
                dataD["alarm"] = False

    def qr_validate(self):
        dataD["alarm"] = False
        # set up camera object
        cap = cv2.VideoCapture(-1)

        # QR code detection object
        detector = cv2.QRCodeDetector()
        while True:
            # get the image
            _, img = cap.read()
            # get bounding box coords and data
            data['content'], bbox, _ = detector.detectAndDecode(img)

            # if there is a bounding box, draw one, along with the data
            if (bbox is not None):

                cv2.putText(img, data['content'], (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 0), 2)
                cv2.imshow("code detector", img)

                if data['content']:
                    mycursor = mydb.cursor()
                    mycursor.execute("select student_password from student where student_password = %s",
                                     [data['content']])
                    fetched_data = mycursor.fetchone()

                    if fetched_data is None:
                        # Buzzer setup
                        GPIO.setwarnings(False)
                        GPIO.setmode(GPIO.BOARD)
                        GPIO.setup(10, GPIO.OUT)
                        # control Buzzer when data received invalid- set output to HIGH
                        for i in range(0, 6):
                            for pulse in range(60):
                                GPIO.output(10, True)
                                time.sleep(0.001)
                                GPIO.output(10, False)
                                time.sleep(0.001)
                            time.sleep(0.02)
                        publish(myChannel, {"data": "invalid"})
                        data['Found'] = "false"
                        cap.release()
                        cv2.destroyAllWindows("code detector")
                        return
                    else:
                        if fetched_data[0] == data['content']:
                            print("data Valid")
                            # LED setup
                            GPIO.setmode(GPIO.BOARD)
                            GPIO.setup(8, GPIO.OUT)

                            # control LED when data received - set output to HIGH
                            for i in range(0, 1):
                                GPIO.output(8, True)
                                time.sleep(0.5)
                                GPIO.output(8, False)
                                time.sleep(0.5)
                            publish(myChannel, {"data": "valid"})
                            GPIO.cleanup()
                            mycursor.close()
                            data['Found'] = "true"
                            cap.release()
                            cv2.destroyAllWindows("code detector")
                            return



if __name__ == '__main__':
    app.run(host='192.168.43.136', port=8080)
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels(myChannel).execute()

    # server = Server(app.wsgi_app)
    # server.serve()


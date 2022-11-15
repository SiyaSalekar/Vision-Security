import cv2
from flask import Flask, render_template, request, redirect
import os
from livereload import Server
from flask_mysqldb import MySQL
import bcrypt


app = Flask(__name__)

# # database connect
app.config['MYSQL'] = 'localhost'
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = 'vision-security'

mysql = MySQL(app)

# database connect endRegion

# # pubnub
# from pubnub.callbacks import SubscribeCallback
# from pubnub.enums import PNStatusCategory
# from pubnub.pnconfiguration import PNConfiguration
# from pubnub.pubnub import PubNub
#
# pnconfig = PNConfiguration()
#
# pnconfig.subscribe_key = 'sub-c-babca055-8ae8-4cbb-87e3-d1927bc7826a'
# pnconfig.publish_key = 'pub-c-7b7bf3ef-a5df-4ec8-9bb2-f70cc90f6c86'
# pnconfig.user_id = "siya-machine"
# pubnub = PubNub(pnconfig)
#
# def my_publish_callback(envelope, status):
#     # Check whether request successfully completed or not
#     if not status.is_error():
#         pass  # Message successfully published to specified channel.
#     else:
#         pass  # Handle message publish error. Check 'category' property to find out possible issue
#         # because of which request did fail.
#         # Request can be resent using: [status retry];
#
# class MySubscribeCallback(SubscribeCallback):
#     def presence(self, pubnub, presence):
#         pass  # handle incoming presence data
#
#     def status(self, pubnub, status):
#         if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
#             pass  # This event happens when radio / connectivity is lost
#
#         elif status.category == PNStatusCategory.PNConnectedCategory:
#             # Connect event. You can do stuff like publish, and know you'll get it.
#             # Or just use the connected event to confirm you are subscribed for
#             # UI / internal notifications, etc
#             pubnub.publish().channel('siyas-channel').message('Hello world!').pn_async(my_publish_callback)
#         elif status.category == PNStatusCategory.PNReconnectedCategory:
#             pass
#             # Happens as part of our regular operation. This event happens when
#             # radio / connectivity is lost, then regained.
#         elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
#             pass
#             # Handle message decryption error. Probably client configured to
#             # encrypt messages and on live data feed it received plain text.
#
#     def message(self, pubnub, message):
#         # Handle new message stored in message.message
#         print(message.message)
#
# pubnub.add_listener(MySubscribeCallback())
#
# pubnub.subscribe().channels('siyas-channel').execute()
# pubnub endRegion

@app.route("/", methods = ["GET","POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        return render_template("greet.html", name=request.form.get("name", "World"))


@app.route("/register",methods=["POST"])
def register():

    student_id = request.form.get("student_id")
    name = request.form.get("student_name")
    #convert passwd to bytes
    passwd = request.form.get("password").encode()

    #hashing password
    password = bcrypt.hashpw(passwd, bcrypt.gensalt())
    password_store = str(password)

    if not student_id:
        return render_template("error.html", message="Invalid ID")
    if not name:
        return render_template("error.html", message="Enter Name")

    cursor = mysql.connection.cursor()
    cursor.execute("insert into student(name, student_id, password) values (%s, %s, %s) ", (name, student_id, password_store))
    mysql.connection.commit()
    cursor.close()
    return redirect("/")

@app.route("/qrgenerate")
def qrscan():
    global data
    # set up camera object
    cap = cv2.VideoCapture(0)

    # QR code detection object
    detector = cv2.QRCodeDetector()
    while True:
        # get the image
        _, img = cap.read()
        # get bounding box coords and data
        data, bbox, _ = detector.detectAndDecode(img)

        # if there is a bounding box, draw one, along with the data
        if (bbox is not None):

            cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)
            if data:
                cursor = mysql.connection.cursor()
                cursor.execute("select password from student where password = %s", [data])
                fetched_data = cursor.fetchone()

                if fetched_data is None:
                    print("INVALID DATA")
                    return render_template("qr-code.html", someVariable="Invalid")
                else:
                    if fetched_data[0] == data:
                        print("data found: ", data)
                        cursor.close()
                        return render_template("qr-code.html", someVariable=data)


        # display the image preview
        cv2.imshow("code detector", img)
        if (cv2.waitKey(1) == ord("q")):
            break

    # free camera object and exit
    cap.release()
    cv2.destroyAllWindows()




# generate QR code
# @app.route('/qrgenerate/studentID')
# def generateCode(studentID):
#     qr = qrcode.QRCode(version=1,
#                        error_correction=qrcode.constants.ERROR_CORRECT_M,
#                        box_size=10,border=4)
#     qr.add_data(studentID)
#     qr.make(fit=True)
#     img = qr.make_image(fill_color='green', back_color = 'white')
#     img.save(f"templates/images/{studentID}.png")
#     return render_template("index.html")
# endRegion generate QR code



if __name__ == '__main__':
    #app.run(host='192.168.43.136',port=9000)
    server = Server(app.wsgi_app)
    server.serve()




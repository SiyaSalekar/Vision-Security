import threading

import cv2
import RPi.GPIO as GPIO
import time

data={}

PIR_pin = 17
LED_pin = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(PIR_pin,GPIO.IN)#PIR
GPIO.setup(PIR_pin,GPIO.OUT)#Buzzer
pwm=GPIO.PWM(PIR_pin,500)
#pubnub channel
PIR_channel="PIR-channel"



class PIR_pin:
    pass
def start_webcam ():
cap = cv2.VideoCapture
while True:
    ret, img=cap.read()
    cv2.imshow('webcam', img)
    k=cv2.waitKey(10)
    if k==27:
        break;
cap.release()
cv2.destroyAllWindows


def motion_detection():
    data["alarm"] = False
    print("sensor started")
    trigger = False
    while True:
        if GPIO.input(PIR_pin):
            publishToPubNub(PIR_channel, {"motion": "yes"})
            print("motion detected")
            beep(4)

            data["motion"] = 1
        elif trigger:
            data["motion"] = 0
            publishToPubNub(PIR_channel, {"motion": "no"})
            trigger = False
            print("no motion")
        time.sleep(1)

        if motion_detection() == True:
            # call to start webcam

            web_cam = threading.Thread(target=start_webcam(True))
            web_cam.start()
            web_cam.join()

        else:
            pubnubmsg = "not in range"
            print(pubnubmsg)


def beep(repeat):
    for i in range(0, repeat):
        for pulse in range(60):
            pwm.start(100)
            time.sleep(0.001)
            pwm.stop()
            time.sleep(0.001)
        time.sleep(0.02)


def publishToPubNub(channel, message):
    pubnub.publish().channel(PIR_channel).message(message).pn_async(my_publish_callback)




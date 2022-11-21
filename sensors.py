
#led.py

from time import sleep
import RPi.GPIO as GPIO
#library for webcamera
import cv2
import os
from datetime import datetime
import time
#threading library
import threading
#pubnub imports
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
#os import to get directory structure
import os

#PubnuBconfiguration publish key /subscribe key and unique ID
pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-af22249a-f784-4ef2-b38f-8515e37d174e'
pnconfig.publish_key = 'pub-c-dc785617-6b97-4cd5-94a4-fdb7c4807921'
pnconfig.user_id = "a75ca08c-683b-11ed-9022-0242ac120002"
pubnub = PubNub(pnconfig)

#location of snapshots taken from webcam
image_directory=os.getcwd()+'/~temp_snaps/'


data={}
sensorList=["pir","buzzer""ultrasound","webcamera"]
#setting the mode of board
GPIO.setmode(GPIO.BCM)
#ultrasound sensors
ECHO=13
TRIG=19

   
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
#pin for led
LED_pin=18
#motion detection PIN
PIR_pin=17
#buzzer pin
BUZZER_pin=26
#RGB led pins
red_pin=21
green_pin=20
blue_pin=16

#setting the RGB pins
GPIO.setup(red_pin,GPIO.OUT)
GPIO.setup(green_pin,GPIO.OUT)
GPIO.setup(blue_pin,GPIO.OUT)


GPIO.setwarnings(False)
GPIO.setup(LED_pin,GPIO.OUT)#LED
GPIO.setup(PIR_pin,GPIO.IN)#PIR
GPIO.setup(BUZZER_pin,GPIO.OUT)#Buzzer

pwm=GPIO.PWM(BUZZER_pin,500)
#pubnub channel
PIR_channel="PIR-channel"
#follwoing are methods to show RGB led different colors based on their RGb values 1 or 0
def green():
	GPIO.output(red_pin,1)
	GPIO.output(green_pin,0)
	GPIO.output(blue_pin,1)
def red():
	GPIO.output(red_pin,0)
	GPIO.output(green_pin,1)
	GPIO.output(blue_pin,1)
def  blue():
	GPIO.output(red_pin,1)
	GPIO.output(green_pin,1)
	GPIO.output(blue_pin,0)
def yellow():
	GPIO.output(red_pin,0)
	GPIO.output(green_pin,0)
	GPIO.output(blue_pin,1)
def purple():
	GPIO.output(red_pin,0)
	GPIO.output(green_pin,1)
	GPIO.output(blue_pin,0)

#motion detection method
def motion_detection():
    data["alarm"] =False
    print("sensor started")
    trigger=False
    while True:
        if GPIO.input(PIR_pin):
            red()
            
            publishToPubNub(PIR_channel,{"motion":"yes"})
            print("motion detected")
            beep(4)
           
            data["motion"]=1
        elif trigger:
            data["motion"]=0
            publishToPubNub(PIR_channel,{"motion":"no"})
            trigger=False
            print("no motion")
        time.sleep(1)
#beep method called by motion_detection()
def beep(repeat):
    for i in range(0,repeat):
        for pulse in range(60):
            pwm.start(100)
           
            #GPIO.output(BUZZER_pin,True)
						
            GPIO.output(LED_pin,1)
            red()	
            time.sleep(0.001)
            pwm.stop()
            #GPIO.output(BUZZER_pin,False)
            GPIO.output(LED_pin,0)
            yellow()
            time.sleep(0.001)
        time.sleep(0.02)
    

#pubnul publish method wrapped in local method to deal with
#specific messages pertinent to each sensor
def publishToPubNub(channel,message):
     pubnub.publish().channel(PIR_channel).message(message).pn_async(my_publish_callback)


#wemcamera method to snap pictures
# pitures are stored locally for a while in ~/~temp_snaps folder
def web_camera_snap(snap):
    
    cam =cv2.VideoCapture(0)
    
    while(snap):
        print(snap)
        
        ret,image=cam.read()
       # cv2.imshow("myimage",image)
        #cant show image . we aint got a x-server display
       
        #3 seconds in total
        if cv2.waitKey(5000):
            dt=datetime.now()
            ts=datetime.timestamp(dt)
            image_name=("%s%s.jpeg" %(image_directory,ts))
            cv2.imwrite(image_name,image)
            publishToPubNub(PIR_channel,{'mugshot':'no display'})
            snap=False
            break
    cam.release()    
    cv2.destroyAllWindows()

def ultra_sound_get_distance():
    #this variable is used by ultra_sound_distance method to loop
    #untill user is within accepted range for mug to be taken 10 -100 cm
    #when condition is satisfied 
    distanceRange=True    

    while distanceRange:
        #doint the measurement flash purple
        purple()
        time.sleep(2)
        msg=("Distance measurement in progress")
        print(msg)
     
        GPIO.output(TRIG,False)
        
        green()
        print("waiting for sensor to settle")
        time.sleep(2)
        GPIO.output(TRIG,True)
        time.sleep(0.00001)

        GPIO.output(TRIG,False)
        while GPIO.input(ECHO)==0:
           
            pulse_start=time.time()
            #doint measurement led is green
            green()
        while GPIO.input(ECHO)==1:
            #done led is red
            pulse_end=time.time()
            red()
        pulse_duration=pulse_end-pulse_start
        distance=pulse_duration*17150
        distance=round(distance,2)
        if distance >10 and distance <100:
            print(distance)
            distanceRange=False
            #call web_cam_snap
            publishToPubNub(PIR_channel,{'distance':distance})
            web_cam=threading.Thread(target=web_camera_snap(True))
            web_cam.start()
            web_cam.join()
            
        else:
            pubnubmsg="not in range"
            print(pubnubmsg)


	
#pubnub API methods
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
            
            print("MySubscribeCallback")
           	   
	  
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
                print("def message")
                msg=message.message
                key=list(msg.keys())
                if(key[0])=="event": 
                    self.handleEvent(msg)
                print(message.message)
        except Exception as e:
                print("Received:",message.message)
                print(e)
                pass
    def handleEvent():
        global data
        eventData=msg["event"]
        key=list(eventData.keys())
        print(key)
        if key[0] in sensorList =="motion":
            if eventData[key[0]] is True:
                data["alarm"]=True
            elif eventData[key[0]]is False:
                data["alarm"]=False

if __name__=="__main__":
    #pir_thread=threading.Thread(target=motion_detection)
    #pir_thread.start()
    #web_camera_thread=threading.Thread(target=web_camera_snap(True))
    ultra_sound=threading.Thread(target=ultra_sound_get_distance())
    ultra_sound.start()
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels(PIR_channel).execute()

#ultra_sound_get_distance()
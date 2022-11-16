from gpiozero import LED
from gpiozero import MotionSensor

white_led = LED(18)
pir = MotionSensor(17)
white_led.off()

while True:
    pir.wait_for_motion()
    print("Motion Detected")
    white_led.on()
    pir.wait_for_no_motion()
    white_led.off()
    print("Motion Stopped")

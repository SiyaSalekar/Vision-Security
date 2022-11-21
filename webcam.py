import cv2
import os 
from datetime import datetime

from datetime import datetime






#get directory where to save images
image_directory=os.getcwd()+'\static\images\\~temp_webcam\\'

cam =cv2.VideoCapture(0)
while True:
	
	ret,image=cam.read()
	cv2.imshow('myImage',image)
	
	if cv2.waitKey(1) & 0xFF==ord('q'):
		dt = datetime.now()
		#timestamp will be name of image
		ts = datetime.timestamp(dt)
		image_name=("%s%s.jpeg" %(image_directory,ts) )
		cv2.imwrite(image_name,image)
		break
#release cam resource
cam.release()
#python windows  destroyed
cv2.destroyAllWindows()

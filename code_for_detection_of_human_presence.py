import cv2
import numpy as np




face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
up_cascade=cv2.CascadeClassifier('haarcascade_upperbody.xml')
reye_cascade=cv2.CascadeClassifier('haarcascade_righteye_2splits.xml')
 
 
cap=cv2.VideoCapture(0)
while True:
    ret,img=cap.read()
    
    a=0
    b=0
    c=0

    global centre    
    
    gray =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
    
    #body= body_cascade.detectMultiScale(gray,1.3,4)
    face= face_cascade.detectMultiScale(gray,1.3,4)
    #up=up_cascade.detectMultiScale(gray,1.3,4)
    #right=reye_cascade.detectMultiScale(gray,1.3,4)
        
    
    
    for (x,y,w,h) in face:
        cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0) ,2)
        centre=round((2*x+w)/2)

    print(centre)
    

##        print(face)
##        print("room occupied||lights on")
        
    (h, w) = img.shape[:2] #w:image-width and h:image-height
    cv2.circle(img, (w//2, h//2), 7, (255, 255, 255), -1)
    img=cv2.line(img,(round(w/2),0),(round(w/2),h),(255,0,0),2)
    
    if centre<(w//2):
        cv2.putText(img,"left".format(),(30,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        a=1
        
    elif centre>(w//2):
        cv2.putText(img,"right".format(),(30,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        b=2
    else:
        cv2.putText(img,"centre".format(),(30,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        

    
##        
##    ##for (x,y,w,h) in up:
##        cv2.rectangle(img,(x,y),(x+w,y+h), (0,0,255) ,2)
##        b=1
##        print(up)
##        print("room occupied||lights on")
    
##    for (x,y,w,h) in right:
##        cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,255) ,2)
##        c=1
##        print(right)
##        print("room occupied||lights on")
    
##    if (l_flag==1):
##        cv2.putText(img,"left".format(),(30,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
##    elif (r_flag==1):
##        
##        cv2.putText(img,"right".format(),(30,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
##    else:
##        cv2.putText(img,"centre".format(),(30,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
        
##        cv2.putText(img,"LIGHTS ACTIVE".format(),(300,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)
        
    cv2.imshow('img',img)
    
    
    k=cv2.waitKey(30) & 0xff
    if k==27:
        break
    
    
cap.release()
cv2.destroyAllWindows()

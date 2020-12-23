import cv2
import numpy as np
import pygame
pygame.init() 

win = pygame.display.set_mode((500, 500))
#win = pygame.display.set_mode((500, 500))
p = 250
q = 500

vel2=1
width = 20
height = 20
a=False
b=False

font = pygame.font.Font('freesansbold.ttf', 10)
text = font.render('GoingLeft', True, (0,255,0), (0,0,255))

global centre

centre=0

face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
##up_cascade=cv2.CascadeClassifier('haarcascade_upperbody.xml')
##reye_cascade=cv2.CascadeClassifier('haarcascade_righteye_2splits.xml')

 
cap=cv2.VideoCapture(0)
run=True
while run:
    ret,img=cap.read()
    
    pygame.time.delay(10)
    vel1 = 1
    c=0
    
    
   

       
    
    gray =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
    
    #body= body_cascade.detectMultiScale(gray,1.3,4)
    face= face_cascade.detectMultiScale(gray,1.3,4)
    
        
    
    
    for (x,y,w,h) in face:

        cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0) ,2)

        centre=round((2*x+w)/2)

 
        
    (h, w) = img.shape[:2] #w:image-width and h:image-height
    cv2.circle(img, (w//2, h//2), 7, (255, 255, 255), -1)
    img=cv2.line(img,((round(w/2)-60),0),((round(w/2)-60),h),(255,0,0),1)
    img=cv2.line(img,((round(w/2)-150),0),((round(w/2)-150),h),(255,255,0),1)
    
    img=cv2.line(img,((round(w/2)+60),0),((round(w/2)+60),h),(255,0,0),1)
    img=cv2.line(img,((round(w/2)+150),0),((round(w/2)+150),h),(255,255,0),1)
    
    
    
        
    if centre>((w//2)+60):
        if centre>((w//2)+150):
            cv2.putText(img,"hard right".format(),(30,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            vel1=0
            a=False
            b=True
        else:
            cv2.putText(img,"right".format(),(30,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            a=False
            b=True
            
    elif centre<((w//2)-60):
        if centre<((w//2)-150):
            cv2.putText(img,"hard left".format(),(30,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            vel1=0
            a=True
            b=False
        else:
            
            cv2.putText(img,"left".format(),(30,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            a=True
            b=False
    else:
        
        cv2.putText(img,"centre".format(),(30,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        a=False
        b=False
        
        


    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False


    keys = pygame.key.get_pressed()
    if a==True and b==False:
    
        
        p -= vel2
        #text = font.render('GoingLeft', True, (0,255,0), (0,0,255))
        textRect = text.get_rect()
        textRect.center = (250,250)

        win.blit(text, textRect)
 
        
    if a==False and b==True:

        p += vel2
    q-=vel1


        
    if keys[pygame.K_DOWN] and q<500-height:
        q += vel
    win.fill((0, 255, 255))
    pygame.draw.rect(win, (255, 0,0 ), (p, q, width, height))
    pygame.display.update()


    cv2.imshow('img',img)

 
    k=cv2.waitKey(30) & 0xff
    if k==27:
        break
pygame.quit()
cap.release()
cv2.destroyAllWindows()

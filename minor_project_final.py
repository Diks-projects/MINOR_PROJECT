import cv2
import numpy as np
import dlib
from math import hypot
import pygame
pygame.init() 

win = pygame.display.set_mode((500, 500))
#win = pygame.display.set_mode((500, 500))
p = 250
q = 500
vel2= 1




width = 20
height = 20
a=False
b=False
#font = pygame.font.Font('freesansbold.ttf', 10)
#text = font.render('GoingLeft', True, (0,255,0), (0,0,255))

global centre
centre=0

face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()

predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

font=cv2.FONT_HERSHEY_PLAIN

def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point =(facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
        
    #hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
    #ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)

    hor_line_length=hypot((left_point[0]-right_point[0]),(left_point[1]-right_point[1]))
        
    ver_line_length =hypot((center_top[0]-center_bottom[0]),(center_top[1]-center_bottom[1]))

    ratio=hor_line_length/ver_line_length

    return ratio

blinking_frame=0
run = True
while run:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    face= face_cascade.detectMultiScale(gray,1.3,4)
    pygame.time.delay(10)
    vel1=1
    

    for (x,y,w,h) in face:
        cv2.rectangle(frame,(x,y),(x+w,y+h), (0,255,0) ,2)
        centre=round((2*x+w)/2)

    #print(centre)

    (h, w) = frame.shape[:2] #w:image-width and h:image-height
    cv2.circle(frame, (w//2, h//2), 7, (255, 255, 255), -1)
    #img=cv2.line(frame,(round(w/2),0),(round(w/2),h),(255,0,0),2)
    frame=cv2.line(frame,((round(w/2)-60),0),((round(w/2)-60),h),(255,0,0),1)
    img=cv2.line(frame,((round(w/2)-150),0),((round(w/2)-150),h),(255,255,0),1)

    
    frame=cv2.line(frame,((round(w/2)+60),0),((round(w/2)+60),h),(255,0,0),1)
    img=cv2.line(frame,((round(w/2)+150),0),((round(w/2)+150),h),(255,255,0),1)
    


   if centre>((w//2)+60):
        if centre>((w//2)+150):
            cv2.putText(frame,"hard right".format(),(30,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            vel1=0
            a=False
            b=True
        else:
            cv2.putText(frame,"right".format(),(30,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            a=False
            b=True
            
    elif centre<((w//2)-60):
        if centre<((w//2)-150):
            cv2.putText(frame,"hard left".format(),(30,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            vel1=0
            a=True
            b=False
        else:
            
            cv2.putText(frame,"left".format(),(30,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            a=True
            b=False
    else:
        
        cv2.putText(frame,"centre".format(),(30,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        a=False
        b=False
        
        
    for face in faces:
        #x, y = face.left(), face.top()
        #x1, y1 = face.right(), face.bottom()
        #cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)
        landmarks = predictor(gray, face)

        #detect blinking
        
        left_eye_ratio=get_blinking_ratio([36,37,38,39,40,41],landmarks)
        right_eye_ratio=get_blinking_ratio([42,43,44,45,46,47],landmarks)
        blinking_ratio=(left_eye_ratio + right_eye_ratio)/2
        if (blinking_ratio>5.3):
            cv2.putText(frame,"BLINKING",(50,200),font,3,(0,255,0))
            blinking_frame=blinking_frame+1

##            if blinking_frame==4:
##                print("hela bala")
##                blinking_frame=0

                
        for event in pygame.event.get():
            
        
            if event.type==pygame.QUIT:
                
                run=False


        keys = pygame.key.get_pressed()

        if blinking_frame==4:
            pygame.time.wait(5000)

            print("STOP")

            blinking_frame=0

        q-=vel1
        if a==True and b==False:
                
                    
            p -= vel2
            #text = font.render('GoingLeft', True, (0,255,0), (0,0,255))
                   
                    
        if a==False and b==True:

            p += vel2



                    
        if keys[pygame.K_DOWN] and q<500-height:
            q += vel1
        win.fill((0, 255, 255))
        pygame.draw.rect(win, (255, 0,0 ), (p, q, width, height))
        pygame.display.update()



        
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()


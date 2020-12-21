import cv2
import numpy as np
import dlib
from math import hypot

global centre
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
def get_gaze_ratio(eye_points,landmarks):
    left_eye_region=np.array([(landmarks.part(eye_points[0]).x, landmarks.part(eye_points[0]).y),

                                 (landmarks.part(eye_points[1]).x, landmarks.part(eye_points[1]).y),
                                 (landmarks.part(eye_points[2]).x, landmarks.part(eye_points[2]).y),
                                 (landmarks.part(eye_points[3]).x, landmarks.part(eye_points[3]).y),
                                 (landmarks.part(eye_points[4]).x, landmarks.part(eye_points[4]).y),
                                 (landmarks.part(eye_points[5]).x, landmarks.part(eye_points[5]).y)],np.int32)
    #cv2.polylines(frame,[left_eye_region],True,(0,0,255),2)

        
    height,width,_ =frame.shape
    mask=np.zeros((height,width),np.uint8)
        
    cv2.polylines(mask,[left_eye_region],True,255,2)
    cv2.fillPoly(mask,[left_eye_region],255)
    eye=cv2.bitwise_and(gray,gray,mask=mask)

    min_x=np.min(left_eye_region[:, 0])
    max_x=np.max(left_eye_region[:, 0])
    min_y=np.min(left_eye_region[:, 1])
    max_y=np.max(left_eye_region[:, 1])


    gray_eye= eye[min_y:max_y, min_x:max_x]

        #gray_eye=cv2.cvtColor(eye,cv2.COLOR_BGR2GRAY)
    _, threshold_eye=cv2.threshold(gray_eye,70,255,cv2.THRESH_BINARY)

    height,width=threshold_eye.shape
    left_side_threshold= threshold_eye[0:height, 0: int(width/2)]
    left_side_white=cv2.countNonZero(left_side_threshold)
        
    right_side_threshold= threshold_eye[0:height, int(width/2): width]
    right_side_white=cv2.countNonZero(right_side_threshold)

    if(left_side_white==0):

        gaze_ratio=1
    elif(right_side_white==0):
        gaze_ratio=5

    else:

        gaze_ratio = left_side_white/right_side_white

    return gaze_ratio

blinking_frame=0
while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    face= face_cascade.detectMultiScale(gray,1.3,4)

    for (x,y,w,h) in face:
        cv2.rectangle(frame,(x,y),(x+w,y+h), (0,255,0) ,2)
        centre=round((2*x+w)/2)

    #print(centre)

    (h, w) = frame.shape[:2] #w:image-width and h:image-height
    cv2.circle(frame, (w//2, h//2), 7, (255, 255, 255), -1)
    img=cv2.line(frame,(round(w/2),0),(round(w/2),h),(255,0,0),2)
    
    if centre<(w//2):
        cv2.putText(frame,"left".format(),(30,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        a=1
        
    elif centre>(w//2):
        cv2.putText(frame,"right".format(),(30,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        b=2
    else:
        cv2.putText(frame,"centre".format(),(30,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

        
    for face in faces:
        #x, y = face.left(), face.top()
        #x1, y1 = face.right(), face.bottom()
        #cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)
        landmarks = predictor(gray, face)

        #detect blinking
        
        left_eye_ratio=get_blinking_ratio([36,37,38,39,40,41],landmarks)
        right_eye_ratio=get_blinking_ratio([42,43,44,45,46,47],landmarks)
        blinking_ratio=(left_eye_ratio + right_eye_ratio)/2
        if (blinking_ratio>5.2):
            cv2.putText(frame,"BLINKING",(50,150),font,3,(255,0,0))
            blinking_frame=blinking_frame+1

            if blinking_frame==4:

                print("hela bala")
                blinking_frame=0


        #gaze controll


        gaze_ratio_left_eye= get_gaze_ratio([36,37,38,39,40,41],landmarks)
        gaze_ratio_right_eye= get_gaze_ratio([42,43,44,45,46,47],landmarks)

        gaze_ratio=(gaze_ratio_left_eye+gaze_ratio_right_eye)/2
##
##        if gaze_ratio<0.7:
##            cv2.putText(frame,"RIGHT",(50,100),font,2,(0,0,255),3)
##        elif 0.8<gaze_ratio<1.6:
##            cv2.putText(frame,"CENTER",(50,100),font,2,(0,0,255),3)
##        else:
##            cv2.putText(frame,"LEFT",(50,100),font,2,(0,0,255),3)
        
        #cv2.putText(frame,str(left_side_white),(50,100),font,2,(0,0,255),3)
        #cv2.putText(frame,str(right_side_white),(50,150),font,2,(0,0,255),3)
        
        #threshold_eye=cv2.resize(threshold_eye, None, fx=5, fy=5)        
        #eye=cv2.resize(gray_eye, None, fx=5, fy=5)

        #cv2.imshow("eye",eye)
        #cv2.imshow("threshold",threshold_eye)
        #cv2.imshow('left_eye',left_eye)
        
        #cv2.imshow('left',left_side_threshold)
        #cv2.imshow('right',right_side_threshold)
        
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()

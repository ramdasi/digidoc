import cv2
import numpy as np
cap = cv2.VideoCapture(0)

while(1):
    _,frame = cap.read()
    blur = cv2.GaussianBlur(frame,(5,5),0)
    blur = cv2.GaussianBlur(blur,(5,5),0)
    edges = cv2.Canny(blur,40,100)
    
    lines = cv2.HoughLines(edges,1,np.pi/180,100)
    doclines = []
    #frame = np.array(frame)*0
    try:
        
        for p in lines:
            r1,theta1=p[0]
            for q in lines:
                r2,theta2=q[0]
                print(theta1-theta2)
                if((np.abs(theta1-theta2)<(np.pi*3/180)) and (np.abs(r1-r2)>20)):
                    doclines.append(p)
                    doclines.append(q)
                    
        
        for i in doclines:
            r,theta = i[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*r
            y0 = b*r
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(frame,(x1,y1), (x2,y2), (0,0,255),2) 
    except:
        pass
    
    cv2.imshow('',frame)
    cv2.imshow('edges',edges)
    


    cv2.waitKey(1)
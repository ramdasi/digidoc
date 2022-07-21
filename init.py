import cv2
import numpy as np
cap = cv2.VideoCapture(1)

max_perspective = np.pi*10/180




def select_doclines(lines):
    doclines=[]
    for i in range(len(lines)):
        p= lines[i]
        r1,theta1=p[0]
        for j in range(i+1,len(lines)):
            q = lines[j]
            r2,theta2=q[0]
            if((np.abs(theta1-theta2)<max_perspective) and (np.abs(r1-r2)>50)):
                doclines.append([p])
                doclines.append([q])
    return doclines

def border_detect(doclines):
    
    inclination = doclines[0][0][0][1]
    # max min min max
    
    borders = [[0,0],[1000,0],[1000,0],[0,0]]
    
    for i in doclines:
        r,theta = i[0][0]
        if(np.abs(theta-inclination)<max_perspective):
            if(r>borders[0][0]):
                borders[0][0]=r
                borders[0][1]=theta
            if(r<borders[1][0]):
                borders[1][0]=r
                borders[1][1]=theta
        else:
            if(r>borders[3][0]):
                borders[3][0]=r
                borders[3][1]=theta
            if(r<borders[2][0]):
                borders[2][0]=r
                borders[2][1]=theta
                
    return borders



def intersection(line1, line2):
    b1,theta1 = line1
    b2,theta2 = line2
    if(np.abs(theta1-theta2)<np.pi*50/180):
        return []
    A = np.array([
        [np.cos(theta1), np.sin(theta1)],
        [np.cos(theta2), np.sin(theta2)]
    ])
    b = np.array([[b1], [b2]])
    x, y = np.linalg.solve(A, b)
    x, y = int(np.round(x)), int(np.round(y))
    if(x<0 or y<0):
        return []
    return (x, y)




while(1):
    _,frame = cap.read()
    blur = cv2.GaussianBlur(frame,(5,5),0)
    blur = cv2.GaussianBlur(blur,(5,5),0)
    edges = cv2.Canny(blur,50,70)
    lines = cv2.HoughLines(edges,1,np.pi/180,80)
    
    try:
        doclines = []
        doclines = select_doclines(lines)
        borders = border_detect(doclines)
        corners=[(),(),(),()]
        
        corners[0] =intersection(borders[0],borders[2])
        corners[2] =intersection(borders[0],borders[3])
        corners[3] =intersection(borders[1],borders[3])
        corners[1] =intersection(borders[1],borders[2])
        for i in corners:
            cv2.circle(frame,i,10,(0,255,0),10)
            
        
        
        for i in borders:
            r,theta = i
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*r
            y0 = b*r
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(frame,(x1,y1), (x2,y2), (0,0,255),2) 
            
            detected =True
            for i in borders:
                if(i[0]==0 or i[0]==1000):
                    detected=False
                

            if(detected):
                matrix = cv2.getPerspectiveTransform(np.float32(corners),np.float32([[0,0],[300,0],[0,360],[300,360]]))
                result = cv2.warpPerspective(frame,matrix,(300,360))
                cv2.imshow('r',result)
    except:
        pass
    
    cv2.imshow('',frame)
    cv2.imshow('edges',edges)



    cv2.waitKey(2)

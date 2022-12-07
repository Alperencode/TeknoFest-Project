import cv2
import numpy as np

# Using haarcascade and Starting Capture
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

while cv2.waitKey(1) == -1:
    # Capture frame-by-frame
    _ , frame = cap.read()
    
    # Turning capture into gray pixels
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Using Face Detection Cascade
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.75, minNeighbors=5)
    
    for (x,y,w,h) in faces:
        
        # Numbers of x_start - y_start - x_end - y_end
        print("Face found: ",x, y, w, h)
        
        # The detected zones (Gray and colored)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # Rectange BGR, thickness, width and height
        color = (0, 0, 255)
        border = 2
        width = x + w
        height = y + h

        # Drawing rectangle
        if faces.all():
            cv2.rectangle(frame, (x, y), (width, height),color, border)
            cv2.putText(frame,"Face Found",(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,0.9,color=color,thickness=2)


    # Display the result frame
    cv2.imshow('Face Detection', frame)

cv2.destroyAllWindows()
from pyzbar.pyzbar import decode
from isbnlib import *
import cv2
import numpy as np

# Global variables
result_dictionary = {}
last_book = ""

def ParseISBN(isbn):
    """
    Parsing the ISBN number
    If ISBN is valid, return the metadata
    Else return False
    """
    if not is_isbn10(isbn) and not is_isbn13(isbn):
        return False
    else:
        return meta(isbn)

def ParseMeta(isbn_meta):
    """
    Parsing the metadata from the ISBN
    If data is valid, update the result dictionary
    """
    global last_book
    for key, value in isbn_meta.items():
        result_dictionary[key] = value

    if isbn_meta["Title"] != last_book:
        for key, value in result_dictionary.items():
            print(f"{key}: {value}")
        last_book = isbn_meta["Title"]
    
def DetectFaces(img):
    """
    Detect faces in the frame
    """
    face_cascade = cv2.CascadeClassifier('sources/haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    for (x,y,w,h) in faces:
            # Numbers of x_start - y_start - x_end - y_end
            print("Face found: ",x, y, w, h)
            
            # The detected zones (Gray)
            roi_gray = gray[y:y+h, x:x+w]

            # Rectange BGR, thickness, width and height
            color = (0, 0, 255)
            border = 2
            width = x + w
            height = y + h

            # Drawing rectangle
            if faces.all():
                cv2.rectangle(img, (x, y), (width, height),color, border)
                cv2.putText(img,"Face Found",(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,0.9,color=color,thickness=2)

def DetectBarcode(img):
    """
    Detect barcode in the frame
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    for barcode in decode(gray):
        isbn = barcode.data.decode('utf-8')
        
        isbn_meta = ParseISBN(isbn)

        if(isbn_meta):
            ParseMeta(isbn_meta)
        else:
            print("Invalid ISBN")

        pts = np.array([barcode.polygon],np.int32)
        # pts = pts.reshape((-1,1,2))
        pts2 = barcode.rect
        cv2.polylines(img,[pts],True,(255,255,255),5)
        
        if isbn_meta:
            cv2.putText(img, isbn_meta["Title"],(pts2[0],pts2[1]-5),cv2.FONT_HERSHEY_SIMPLEX,0.9,color=(255,255,255),thickness=2)

def OutputTXT():
    """
    Output the result dictionary to a txt file
    """
    if result_dictionary:
        with open('output.txt', 'w', encoding='utf-8') as f:
            for key, value in result_dictionary.items():
                if type(result_dictionary[key]) == list:
                    f.write(f"{key}: ")
                    for item in result_dictionary[key]:
                        f.write(f"{item}, ") if item != result_dictionary[key][-1] else f.write(f"{item}")
                    f.write("\n")
                else:
                    f.write(f"{key}: {value}\n")

def GetResult():
    """ Getter for the result dictionary """
    return result_dictionary
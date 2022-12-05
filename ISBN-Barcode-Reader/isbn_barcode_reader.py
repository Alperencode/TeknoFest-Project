import cv2
import numpy as np
from pyzbar.pyzbar import decode
from isbnlib import *

def ParseISBN(isbn):
    if not is_isbn10(isbn) and not is_isbn13(isbn):
        return False
    else:
        return meta(isbn)

def ParseMeta(isbn_meta):
    # global last_book
    # if isbn_meta["Title"] != last_book:
    #     print("Title:", isbn_meta["Title"])
    #     last_book = isbn_meta["Title"]
    print("Kitap:", isbn_meta["Title"])
    for key, value in isbn_meta.items():
        valid_data[key] = value

def OutputTXT():
    with open('output.txt', 'w',encoding='utf-8') as f:
        for key, value in valid_data.items():
            if type(valid_data[key]) == list:
                f.write(f"{key}: ")
                for item in valid_data[key]:
                    f.write(f"{item}, ") if item != valid_data[key][-1] else f.write(f"{item}")
                f.write("\n")
            else:
                f.write(f"{key}: {value}\n")

def main():

    cap = cv2.VideoCapture(0)

    while cv2.waitKey(1) == -1:
        success, img = cap.read()
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
            cv2.polylines(img,[pts],True,(0,255,0),5)
            
            cv2.putText(img,isbn,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,0.9,color=(0,255,0),thickness=2)

        
        cv2.imshow('User',img)
        cv2.imshow('Program',gray)
        cv2.waitKey(1)

if __name__ == "__main__":
    valid_data = {}
    last_book = ""
    main() 
    if valid_data:
        OutputTXT()
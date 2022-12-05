from sources import *

def main():
    cap = cv2.VideoCapture(0)

    while cv2.waitKey(1) == -1:
        success, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        for barcode in sources.decode(gray):
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
    main()
    if GetResult():
        OutputTXT()
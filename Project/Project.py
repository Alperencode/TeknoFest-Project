from sources import *

def main():
    
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)

    while cv2.waitKey(1) == -1:
        # Read the frame
        success, img = cap.read()
        
        # Flip the image for mirror effect
        img_flip = cv2.flip(img,1)

        # Detect faces
        DetectFaces(img_flip)

        # Detect barcode
        DetectBarcode(img_flip)

        # Show the frame
        cv2.imshow('User',img_flip)
        
        cv2.waitKey(1)

    # Output the result
    OutputTXT()

if __name__ == "__main__":
    main()
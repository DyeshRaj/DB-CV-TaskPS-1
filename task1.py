import cv2
import numpy as np

def track_color():
    cap = cv2.VideoCapture(0)  #Starting the webcam
    if not cap.isOpened():  #Too see if the webcam is opened or not(Didn't work in google colab)
        print("Cannot access webcam")
        return

    print("Press X to stop")
    colors = {
        "Yellow": (np.array([20, 100, 100]), np.array([35, 255, 255]), (0, 255, 255)),
        "Red":    (np.array([170, 120, 70]), np.array([180, 255, 255]), (0, 0, 255)),
        "Blue":   (np.array([100, 150, 50]), np.array([140, 255, 255]), (255, 0, 0))
    } #Defining a dictionary of colors with their BGR values for display and HSV for masking


    while True:
        ret, frame = cap.read() #Capturing frame by frame from webcam
        
        if not ret:
            print("Failed to capture frame")
            break

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Converting RGB to HSV 
        for color_name, (lower, upper, bgr) in colors.items():
    
            #Creating a mask that checks the yellow color in the frame
            mask = cv2.inRange(hsv_frame, lower, upper)
    
            #Removing Noise to make sure the tracking is smooth
            k = np.ones((5, 5), np.uint8)
            mask = cv2.erode(mask, k, iterations=1)
            mask = cv2.dilate(mask, k, iterations=2)

            #Finding contours of the masked image
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:  #Tracking 
                l_contour = max(contours, key=cv2.contourArea) #Finding the largest contour
                if cv2.contourArea(l_contour) > 500:
                    x, y, w, h = cv2.boundingRect(l_contour) #Get the coordinates (x,y,w,h) of the rectangle box around the object

                    center_x = x + w // 2 #Finding the center of the tranjectory point
                    center_y = y + h // 2

                    # Draw the rectangle around the object on the original frame
                    # Parameters: image, top-left point, bottom-right point, color (B,G,R), thickness
                    cv2.rectangle(frame, (x, y), (x + w, y + h), bgr, 3)

                    # Add a label
                    cv2.putText(frame, color_name+ " COLOR Detected", (x, y - 10),
                            cv2.FONT_ITALIC, 0.7, (0, 0, 0), 2)
                
            cv2.imshow("Color Tracking frame", frame)  #Display the frame with tracking

        if cv2.waitKey(1) & 0xFF == ord('x'): #Stop condition
            break

    cap.release()
    cv2.destroyAllWindows()
        
if __name__ == "__main__":

    track_color()

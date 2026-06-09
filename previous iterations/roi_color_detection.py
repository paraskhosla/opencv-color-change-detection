import cv2

# Function to perform color detection in the specified region of interest (ROI)
def detect_colors_in_roi(frame, roi):
    # Convert ROI to HSV color space
    roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    # Define color range for detection (example: green color)
    lower_green = (35, 50, 50)
    upper_green = (90, 255, 255)
    
    # Threshold the image to detect the specified color range
    mask = cv2.inRange(roi_hsv, lower_green, upper_green)
    
    # Perform bitwise AND operation to extract the detected color regions
    result = cv2.bitwise_and(roi, roi, mask=mask)
    
    return result

# Main function to capture camera feed and perform color detection in ROI
def main():
    # Open camera capture device (change index as needed)
    cap = cv2.VideoCapture(0)
    
    while True:
        # Read frame from the camera
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Define region of interest (example: focus on center of the frame)
        x, y, w, h = 120, 250, 400, 230
        roi = frame[y:y+h, x:x+w]
        
        # Perform color detection in the ROI
        result = detect_colors_in_roi(frame, roi)
        
        # Display original frame with ROI and detected colors
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('Original Frame', frame)
        cv2.imshow('Detected Colors in ROI', result)
        
        # Exit loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the capture device and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
# In this modification:

# I adjusted the x coordinate to be smaller (100) to move the ROI towards the left of the frame.
# I adjusted the y coordinate to be larger (250) to move the ROI further down in the frame (to simulate an object on the floor).
# I increased the w (width) to 400 to make the ROI wider.
# I decreased the h (height) to 230 to keep the ROI relatively narrow.



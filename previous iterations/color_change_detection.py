##
#Author: Paras Khosla
#Date: 07-06-2024
#
#Final delivered version
#
#Description:Utilizing the OpenCV library, this program is designed to detect color changes by employing pre-defined HSV values for the color Burgandi. 
#            *It further incorporates a Region of Interest (ROI) box to focus on specific areas within the video stream.
#            *It also records video immediately when the program starts and cut the video after 10 seconds if color change detected.
#            *This program Halt the program, if no color change detected for 1 minute(can be changed) and saves the video to the path after closing the program. 
#            *Calculate the video duration and print it on terminal
##

import cv2
import numpy as np
import time
import os

def detect_color_change(frame, roi):
    # Convert BGR image to HSV (Hue, Saturation, Value)
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for the original color in HSV
    lower_color = np.array([100, 150, 0])   # Lower HSV values for the original color
    upper_color = np.array([140, 255, 255])  # Upper HSV values for the original color

    # Threshold the HSV image to get only the original color
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Calculate the percentage of the ROI occupied by the original color
    color_percentage = np.sum(mask == 255) / (roi.shape[0] * roi.shape[1]) * 100

    # Determine if the original color is present
    color_present = color_percentage >= 2  # Adjust threshold as needed

    return color_present, mask

def main():
    # Open camera
    cap = cv2.VideoCapture(0)

    # Define region of interest (example: focus on center of the frame, wider and lower)
    x, y, w, h = 120, 250, 400, 230
    # I adjusted the x coordinate to be smaller (120) to move the ROI towards the left of the frame.
    # I adjusted the y coordinate to be larger (250) to move the ROI further down in the frame (to simulate an object on the floor).
    # I increased the w (width) to 400 to make the ROI wider.
    # I decreased the h (height) to 230 to keep the ROI relatively narrow.

    # Video recording setup
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_path = 'D:/testing/output.avi' #Can make a new video every time
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (640, 480))
    recording = True
    color_change_time = None

    # Counter for color change detection
    change_detected_counter = 0  

    # Timer for detecting no color change for 1 minute
    no_color_change_start_time = time.time()

    # Variable to store initial color presence
    initial_color_present = False
    color_change_detected = False

    # Record start time of video recording
    recording_start_time = None

    while True:

        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            break

        # Extract region of interest
        roi = frame[y:y+h, x:x+w]

        # Detect color presence in the ROI
        color_present, mask = detect_color_change(frame, roi)

        # Draw rectangle around ROI
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the mask showing the original color
        cv2.imshow('Color Mask', mask)

        # Check for initial color presence and subsequent color change
        if initial_color_present:
            if not color_present and not color_change_detected:
                color_change_detected = True
                color_change_time = time.time()
                change_detected_counter += 1
                print(change_detected_counter)  # Print counter when color change is detected
        else:
            initial_color_present = color_present

        # Display text on the top of the frame if color change is detected
        if color_change_detected:
            cv2.putText(frame, 'Color Change Detected', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Start recording time if it's the first detection
            if recording_start_time is None:
                recording_start_time = time.time()

            # Stop recording 10 seconds after color change detected
            if time.time() - color_change_time >= 10:
                recording = False

            # Reset no color change timer
            no_color_change_start_time = time.time()

        # Check if no color change detected for 1 minute
        if time.time() - no_color_change_start_time >= 60:
            print("No color change detected for 1 minute. Color detection program stopped & video is saved.")
            break

        # Display the frame with text
        cv2.imshow('Color change detection program', frame)

        # Write the frame to the video file
        if recording:
            out.write(frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Calculate the duration of the recorded video
    if recording_start_time is not None:
        duration_time = time.time() - recording_start_time
        minutes = int(duration_time // 60)
        seconds = int(duration_time % 60)
        duration = f"{minutes}:{seconds}"
        #print(f"Duration of the recorded video: {duration}")
    else:
        duration = None

    # Release the capture, video writer, and close all windows
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return duration

#Function for debugging the "duration" parameter

def use_duration(duration):
    if duration:
        print(f"Video recording duration: {duration}")
    else:
        print("No video was recorded.")

if __name__ == '__main__':
    duration = main()
    use_duration(duration)




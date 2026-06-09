# import cv2
# import numpy as np
# import time
# import os
# import random

# fileID = ''
# # Counter for color change detection
# color_index = 0

# def get_dominant_color(hsv):
#     # Calculate histogram in the HSV space
#     hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
    
#     # Find the peak in the histogram
#     _, max_val, _, max_loc = cv2.minMaxLoc(hist)
    
#     # Convert the peak location to (Hue, Saturation)
#     hue = max_loc[0]
#     saturation = max_loc[1]
    
#     return (hue, saturation)

# def detect_color_change(current_color, stable_color, threshold=30):
#     if stable_color is None:
#         return True  # Treat first detection as a change to initialize stable_color
    
#     # Calculate the Euclidean distance between the two colors in the HSV space
#     color_diff = np.sqrt((current_color[0] - stable_color[0])**2 + (current_color[1] - stable_color[1])**2)
#     return color_diff > threshold  # Adjust the threshold for detecting color change

# def cameraStart():
#     # Open camera with the specified GStreamer pipeline
#     cap = cv2.VideoCapture(0)
    
#     # give the video a unique id and save it
#     global fileID
#     seed = time.time()
#     random.seed(seed)
#     unique_number = random.randint(1, 100000000000)
#     fileID = f'D:/testing/{unique_number}.avi'

#     # Video recording setup
#     fourcc = cv2.VideoWriter_fourcc(*'XVID')
#     output_path = fileID
#     os.makedirs(os.path.dirname(output_path), exist_ok=True)
#     out = cv2.VideoWriter(output_path, fourcc, 10.0, (640, 480))
#     start_time = time.time()

#     stable_color = None
#     current_color = None

#     # Counter for color change detection
#     global color_index
#     color_index = 0  # Initialize color_index to 0
    
#     stable_count = 0
#     stable_threshold = 15  # Change it for better responsiveness
#     color_change_threshold = 55  # Sensitivity for color change detection

#     first_frame = True  # Flag to detect the first frame with color

#     # Define ROI coordinates
#     x, y, w, h = 120, 250, 400, 230

#     last_color_change_time = time.time()

#     # Variable to track if first color change is detected
#     first_color_change_detected = False

#     # Wait for up to 1 minute for the first color change
#     timeout_duration = 60  # 60 seconds
#     start_waiting_time = time.time()

#     while True:
#         # Capture frame-by-frame
#         ret, frame = cap.read()
#         if not ret:
#             break
        
#         # Extract ROI
#         roi = frame[y:y+h, x:x+w]
        
#         # Convert the ROI to HSV
#         hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
#         # Get the dominant color in the current ROI
#         current_color = get_dominant_color(hsv)
        
#         # Debug statement to print current and stable colors
#         #print(f"Current Color: {current_color}, Stable Color: {stable_color}")
        
#         # Check if the dominant color has changed
#         if detect_color_change(current_color, stable_color, threshold=color_change_threshold):
#             stable_count += 1
#             #print(f"Stable Count: {stable_count}")  # Debug statement
#             if stable_count > stable_threshold:
#                 if first_frame:
#                     color_index = 0  # Initialize color_index to 0 on the first color detection
#                     first_frame = False
#                 else:
#                     color_index += 1

#                 # Update the stable color and reset stable count
#                 stable_color = current_color
#                 stable_count = 0
#                 print(f"Color changed to {color_index}")

#                 # Update last color change time
#                 last_color_change_time = time.time()

#                 # Set first color change detected flag
#                 first_color_change_detected = True

#         else:
#             stable_count = 0

#         # Check if 1 minute has passed without any color change
#         if not first_color_change_detected and time.time() - start_waiting_time >= timeout_duration:
#             # Print timeout message and exit
#             print("Timeout: No color change detected within 1 minute.")
#             duration_time = time.time() - start_time
#             minutes = int(duration_time // 60)
#             seconds = int(duration_time % 60)
#             duration = f"{minutes:02}:{seconds:02}"
#             print(f"Video Duration was: {duration}")

#             # Release the current writer and exit the program
#             out.release()
#             break

#         # Check if 10 seconds have passed since the last color change
#         if time.time() - last_color_change_time >= 10 and first_color_change_detected:
#             # Calculate duration and print
#             duration_time = time.time() - start_time
#             minutes = int(duration_time // 60)
#             seconds = int(duration_time % 60)
#             duration = f"{minutes:02}:{seconds:02}"
#             print(f"Video Duration was: {duration}")

#             # Release the current writer and exit the program
#             out.release()
#             break


#         # Display the current color index on the frame
#         cv2.putText(frame, f"Color Index: {color_index}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
#         # Draw ROI rectangle on the frame for visualization
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

#         # Create a mask for the dominant color
#         lower_bound = np.array([current_color[0] - 10, current_color[1] - 50, 50])
#         upper_bound = np.array([current_color[0] + 10, current_color[1] + 50, 255])
#         mask = cv2.inRange(hsv, lower_bound, upper_bound)
#         mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)  # Convert mask to BGR for visualization

#         # Write the frame into the current video file
#         out.write(frame)
        
#         # Display the frame and mask
#         cv2.imshow('Color Detection', frame)
#         cv2.imshow('Color Mask', mask)
        
#         # Break the loop if 'q' is pressed
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
    
#     # Release the capture and video writer objects, and close all windows
#     cap.release()
#     out.release()
#     cv2.destroyAllWindows()

# if __name__ == '__main__':
#     cameraStart()


import cv2
import numpy as np
import time
import os

def detect_color_change(frame, roi):
    # Convert BGR image to HSV (Hue, Saturation, Value)
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for the original color in HSV
    lower_color = np.array([160, 100, 50])   # Lower HSV values for the original color
    upper_color = np.array([180, 255, 255])  # Upper HSV values for the original color

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
    output_path = 'D:/testing/output.avi' #Can make a new video everytime
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

    # Release the capture, video writer, and close all windows
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()



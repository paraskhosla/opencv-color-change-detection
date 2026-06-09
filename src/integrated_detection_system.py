import cv2
import numpy as np
import time
import os
import couchdb
import serial
import paho.mqtt.client as mqtt

# global variables
startExperiment = 0

# Initialize serial
ser = serial.Serial(
        port="COM5",
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE)  # open serial port USB0 (its the only one they have lmfao)

time.sleep(1) # wait for usb port to open
print(ser.name) # double check what port is used

# Connecting with couchdb Server.
couch = couchdb.Server('http://admin:robot123@localhost:5981/')

# Access Database or Create if there is no existing database.
db_name = 'robotiot'
if db_name in couch:
    db = couch[db_name]
    print("Database Accessed")
else:
    db = couch.create(db_name)
    print("Database does not exist. New database created")
#
#Function to detect a color change
# 
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

#
# PLAY VIDEO
#
prev_message = ""

def play_video(file_path):
    cap = cv2.VideoCapture(file_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Video', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

#
# THIS PART OF THE CODE IS THE MQTT STUFF ABOBA
#
def on_connect(client, userdata, flags, reason_code, properties):  # The callback for when the client connects to the broker 
    print("Connected with result code {reason_code}")  
    # Print result of connection attempt 
    client.subscribe("abobaTest")  
    # Subscribe to the topic “digitest/test1”, receive any messages published on it


def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.   
    msg.payload = msg.payload.decode("utf-8")
    print(str(msg.payload))# Print a received msg
    global prev_message

    # retrieve video file path by ID
    if str(msg.payload[0]).isdigit():
        doc_id = msg.payload
        doc = db[doc_id]
        video_file = doc.get('filepath', None)
        play_video(video_file)

    # start new experiment
    if msg.payload == "START":
        title = prev_message
        global startExperiment
        startExperiment = 1
    #prev_message = title of experiment
    prev_message = msg.payload


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) # Create instance of client with client ID “digi_mqtt_test”
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
client.connect("test.mosquitto.org", 1883, 60)  # Connect to (broker, port, keepalive-time)
client.loop_start()
#
#Main function for Color change detection 
#Recording video
#Ending vido after 10 seconds of color change
#Halting the script if there's no color change with in 1 minute
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
    output_path = 'D:/testing/output.avi' # update to robotiot_recordings/[video filename].avi
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
        # vvv start the sensors and camera here vvv
        if startExperiment == 1:
            buf = ser.readLine()
            content = buf.decode("utf-8")
            print(content.strip())
        

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

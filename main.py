import time
import cv2
from ultralytics import YOLO
from config import *
from signal_controller import TrafficSignal

print("===============================")
print(" AI Traffic Management System")
print("===============================")
print("\nLoading  YOLO Model...")
model = YOLO("yolov8n.pt")

print("✅ YOLO Model Loaded Successfully")
print("\nOpening Video...")
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print("❌ Error: Cannot open video.")
    exit()
print("✅ Video Opened Successfully!")
# -----------------
# Variables
# ----------------
counted_ids = set()
total_count = 0

traffic_density = "LOW"
green_time = GREEN_LOW
signal = TrafficSignal()
last_update = time.time()
previous_density = ""
## ==========
## Main Loop
## ========

while True:

    ret, frame = cap.read()
    if not ret:
        print("\nVideo Finished.")
        break
    ## Track Vehicles
    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml"
    )
    ## Draw Tracking Results
    annotated_frame = results[0].plot()
    # Current Vehicles in frame
    current_vehicle_count = 0
    if results[0].boxes.id is not None:
        current_vehicle_count = len(results[0].boxes.id)
    # Draw Counting Line
    cv2.line(annotated_frame,(0, COUNT_LINE_Y),(annotated_frame.shape[1],COUNT_LINE_Y),(0, 255,0),2)
    # Count Vehicles
    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()
        ids = results[0].boxes.id.cpu().numpy().astype(int)
        for box, track_id in zip(boxes, ids):
            x1, y1, x2, y2 = box
            center_y = int((y1 + y2)/2)
            if center_y > COUNT_LINE_Y and track_id not in counted_ids:
                counted_ids.add(track_id)
                total_count+= 1 
    # Calculate Traffic Density 
    if current_vehicle_count <= LOW_TRAFFIC:
        traffic_density = "LOW"
        green_time = GREEN_LOW
    elif current_vehicle_count <= MEDIUM_TRAFFIC:
        traffic_density = "MEDIUM"
        green_time = GREEN_MEDIUM
    else :
        traffic_density = "HIGH"
        green_time = GREEN_HIGH
    ## ADD line
    if traffic_density != previous_density:
        signal.update_green_time(green_time)
        previous_density = traffic_density
    current_time = time.time()
    if current_time - last_update >= 1:
        signal.tick()
        last_update = current_time
    ## Display Information
    cv2.putText(annotated_frame,f"Current Vehicles :  : {current_vehicle_count}",(20,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.putText(annotated_frame,f"Total Vehicles  :   {total_count}",(20,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    cv2.putText(annotated_frame,f"Traffic Density : {traffic_density}",(20,120),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    cv2.putText(annotated_frame,f"{signal.state} : {signal.remaining_time} sec", (20,160),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255, 255),2)
    # Traffic Signal Box
    ## Dark Background 
    cv2.rectangle(
        annotated_frame,
        (900,20),
        (980,220),
        (40,40,40),
        -1
    )
    # White Border 
    cv2.rectangle(
        annotated_frame,
        (900,20),
        (980,220),
        (255,255,255),
        2
    )
    ## Default off Colors
    red_color = (50, 50, 50)
    yellow_color = (50,50,50)
    green_color = (50,50,50)
    # Turn ON the Active Signal 
    if signal.state == "RED":
        red_color = (0,0,255)
    elif signal.state == "YELLOW":
        yellow_color = (0,255,255)
    elif signal.state == "GREEN":
        green_color = (0,255 , 0)
    # Draw Lights 
    cv2.circle(annotated_frame, (940,60), 20, red_color , -1)
    cv2.circle(annotated_frame, (940 , 120), 20 , yellow_color, -1)
    cv2.circle(annotated_frame, (940,180), 20 , green_color, -1)
    ## Traffic Signal Drawing Ends Here
    # Show Output
    cv2.imshow(WINDOW_NAME, annotated_frame)
    if cv2.waitKey(25) & 0xFF == ord("q"):
        break
## cleanup 
cap.release()
cv2.destroyAllWindows()

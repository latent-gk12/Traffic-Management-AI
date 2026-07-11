from ultralytics import YOLO
import cv2
## load YOLO model
model = YOLO("yolov8n.pt")
# Open video
cap = cv2.VideoCapture("videos/test.mp4")
# Line postion
LINE_Y = 350
## Store counted vehicle IDs
counted_ids = set()
total_count = 0

while cap.isOpened():
    success , frame = cap.read()
    if not success:
        break
    # Track vehicles
    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml"
    )
    annotated = results[0].plot()
    # Draw counting line
    cv2.line(annotated, (0, LINE_Y), (annotated.shape[1],LINE_Y),(0,255,0), 3)
    if results[0].boxes.id is not None:
        boxes = results[0].boxes
        ids = boxes.id.int().cpu().tolist()
        for box, track_id in zip(boxes, ids):
            x1 , y1, x2, y2 = box.xyxy[0]
            center_y = int((y1 + y2)/2)
            if center_y >  LINE_Y and track_id not in counted_ids:
                counted_ids.add(track_id)
                total_count += 1
            cv2.putText(
                annotated,
                f"Vehicle Count: {total_count}",
                (20,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,0,255),
                3
            )

    cv2.imshow("Traffic Counter",annotated)
    if cv2.waitKey(1) & 0xFF== ord("q"):
        break
cap.release()
cv2.destroyAllWindows() 
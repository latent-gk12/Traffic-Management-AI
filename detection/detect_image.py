from ultralytics import YOLO
# load  the YOLOv8 model
model = YOLO("yolov8n.pt")
# Run detection on an image
results = model("images/test.jpg")
vehicle_classes = ["car","bus","truck","motorcycle"]
count = {
    "car":0,
    "bus":0,
    "truck":0,
    "motorcycle":0
}
for box in results[0].boxes:
    cls= int(box.cls[0])
    name= model.names[cls]
    if name in count:
        count[name] += 1
print("\n Vehicle Count")
print("-"*15)
for vehicle in count:
    print(f"{vehicle}: {count[vehicle]}")
total = sum(count.values())
print("-------------")
print(f"Total Vehicles: {total}")

if total <= 10:
    density = "LOW"
elif total <= 25:
    density="MEDIUM"
else:
    density = "HIGH"
print(f"Traffic Density : {density}")
# Smart Traffic Signal
if density == "LOW":
    green_time = 20
elif density =="MEDIUM":
    green_time = 40
else : 
    green_time= 60
print(f"Green Signal Time : {green_time} seconds")

import time
green_time = 10
yellow_time = 3
red_time = 5
print("=== Traffic Signal Simulation ===")
# Green Signal
print("\n🟢 GREEN SIGNAL")
for i  in range(green_time, 0, -1):
    print(f"Green : {i} sec")
    time.sleep(1)
# Yellow Signal
print("\n🟡 YELLOW SIGNAL")
for i in range(yellow_time,0,-1):
    print(f"Yellow : {i} sec")
    time.sleep(1)
# Red Signal
print("\n🔴 RED SIGNAL")
for i in range(red_time,0,-1):
    print(f"Red : {i} sec")
    time.sleep(1)

print("\nCycle Completed")
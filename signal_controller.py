import time
class TrafficSignal:
    def __init__(self):
        self.state = "GREEN"
        self.remaining_time = 30
    def update_green_time(self,seconds):
        self.remaining_time = seconds
        self.state = "GREEN"
    def tick(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
        else:
            if self.state == "GREEN":
                self.state = "YELLOW"
                self.remaining_time = 5
            elif self.state == "YELLOW":
                self.state = "RED"
                self.remaining_time = 10
            elif self.state == "RED":
                self.state = "GREEN"
                self.remaining_time = 30
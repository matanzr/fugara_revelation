import requests 
import json 
import time
from pov_fan import PovFan

server_url = "http://192.168.1.109:3000/"

REGISTER = "register"
ACTION = "action"
headers = {'content-type': 'application/json'}

CLIENT_STATES = ["idle", "loading", "loaded", "drawing"]
CLIENT_ACTIONS = ["idle", "load", "draw"]

class FanClient:
    def __init__(self, fan_id):
        self.is_running = False
        self.fan_id = fan_id
        self.interval = 0.5
        self.state = "idle"
        self.action = "idle"
        self.server_ts = 0

        self.fan = PovFan()

    def send_request(self, endpoint, payload):
        return requests.post(server_url + endpoint, data=json.dumps(payload), headers=headers)

    def register_fan(self):
        payload = {"fanId": self.fan_id}
        res = self.send_request(REGISTER, payload)

        if res.status_code == 200: return True
        else: return False
    
    def send_action(self):
        payload = {
            "fanId": self.fan_id, 
            "state": self.state
            }
        res = self.send_request(ACTION, payload)

        return res.json()

    def play_fan(self, length = 1):        
        self.state = "drawing"
        self.fan.play(length)
    
    def stop_fan(self):        
        # self.fan.stop()
        self.state = "idle"

    def load_sequence(self, name):
        self.state = "loading"

        path = name
        print "loading sequence: ", name
        # self.fan.load_sequence(path)
        self.fan.load_sequence("test_images/fugara_test_image_radial.png") 

        self.state = "loaded"

    def run(self):
        self.is_running = True

        ### register fan on server
        is_registered = False
        print "starting client " + self.fan_id
        while is_registered == False: 
            is_registered = self.register_fan()
            time.sleep(self.interval)
        
        ### client is running until stopped
        print "Successfuly registered with server"
        while self.is_running:
            next_state = self.send_action()
            if next_state["action"] != self.action:
                print "Last state was ", self.action,  "now doing: ", next_state["action"]

                self.action = next_state["action"]
                
                if self.action == "load": self.load_sequence(next_state["animation"])
                if self.action == "idle": self.stop_fan()
                if self.action == "draw": self.play_fan()

            time.sleep(self.interval)

if __name__ == "__main__":
    client = FanClient("test_fan")
    # client.run()

    client.load_sequence("test_images/fugara_test_image_radial.png")
    client.play_fan(5)

    client.load_sequence("test_images/fugara_test_image_radial.png")
    client.play_fan(5)
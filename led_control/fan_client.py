import requests
import json
import time
from pov_fan import PovFan
import random

server_url = "http://192.168.1.15:3000/"
# server_url = "http://0.0.0.0:3000/"


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
        try:
            return requests.post(server_url + endpoint, data=json.dumps(payload), headers=headers)
        except:
            return "Need Restart";


    def register_fan(self):
        payload = {"fanId": self.fan_id}
        res = self.send_request(REGISTER, payload)
        if res == "Need Restart": return "Need Restart";

        if res.status_code == 200: return True
        else: return False

    def send_action(self):
        payload = {
            "fanId": self.fan_id,
            "state": self.state
            }
        res = self.send_request(ACTION, payload)
        if res == "Need Restart": return "Need Restart";
        return res.json()

    def play_fan(self, length = 1):
        self.state = "drawing"
        self.fan.play(length)

    def stop_fan(self):
        self.fan.stop()
        self.state = "idle"

    def load_sequence(self, name):
        self.state = "loading"

        path = name
        print "loading sequence: ", name
        self.fan.load_sequence(path, self.fan_id)
        # self.fan.load_sequence("test_images/fugara_test_image_radial.png", self.fan_id)

        self.state = "loaded"

    def run(self):
        self.is_running = True

        ### register fan on server
        is_registered = False
        print "starting client " + self.fan_id
        while is_registered == False:
            register_fan_res = self.register_fan()
            if register_fan_res != "Need Restart":
                print "register_fan_res"
                is_registered = register_fan_res;
            time.sleep(self.interval)

        ### client is running until stopped
        print "Successfuly registered with server"
        while self.is_running:
            send_action_res = self.send_action()
            if send_action_res == "Need Restart":
                self.run();
                return;

            next_state = send_action_res;
            if next_state["action"] != self.action:
                print "Last state was ", self.action,  "now doing: ", next_state["action"]

                self.action = next_state["action"]

                if self.action == "load": self.load_sequence(next_state["animation"])
                if self.action == "idle": self.stop_fan()
                if self.action == "draw": self.play_fan()

            time.sleep(self.interval)

if __name__ == "__main__":
    client = FanClient(1)
    client.run()

    # client.load_sequence("test_images/fugara_test_image_radial.png")
    # client.play_fan(5)
    #
    # client.load_sequence("test_images/fugara_test_image_radial.png")
    # client.play_fan(5)

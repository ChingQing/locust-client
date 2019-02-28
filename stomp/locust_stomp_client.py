import time
import random
import json
import stomp
import requests
from locust import Locust, TaskSet, events, task
# from deviceID import devices_id


class StompClient(object):
    def __init__(self, host, port):
        self.conn = stomp.Connection10([(host, port)])

    def __del__(self):
        if self.conn:
            print "disconnect..."
            self.conn.disconnect()

    def start(self):
        start_time = time.time()
        try:
            self.conn.start()
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="stomp", name="start", response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="stomp", name="start", response_time=total_time, response_length=0)

    def connect(self):
        start_time = time.time()
        try:
            self.conn.connect()
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="stomp", name="connect", response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="stomp", name="connect", response_time=total_time, response_length=0)
        
    def send(self, body, destination, name=""):
        start_time = time.time()
        try:
            self.conn.send(body=body, destination=destination)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="stomp", name="send "+name, response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="stomp", name="send "+name, response_time=total_time, response_length=0)



class StompLocust(Locust):
    """
    This is the abstract Locust class which should be subclassed. It provides an Stomp client
    that can be used to make Stomp requests that will be tracked in Locust's statistics.
    """
    def __init__(self, *args, **kwargs):
        super(StompLocust, self).__init__(*args, **kwargs)
        self.client = StompClient(self.host, self.port)
        self.client.start()
        self.client.connect()


def random_devid(start=0, end=12):

    did = requests.get("http://200.200.200.235:8888/getdid").text   #get a unique number
    return did


class TestUser(StompLocust):
    host = "200.200.200.200"
    port = 61613
    min_wait = 2000
    max_wait = 2000

    class task_set(TaskSet):
        queuename = "mi.phone.device.queue"
        userId = 19845

        @task(1)
        def send_breath_ex_data(self):
            des = self.queuename
            did = random_devid(0, 10)
            self.client.send(des, "normal")
            msg = {
                "createTime": int(time.time()*1000),
                "deviceId": did,
                "from": "",
                "productId": 136,
                "data": json.dumps({
                    "dataTime":int(time.time()*1000),
                    "deviceId":did,
                    "userId":self.userId,
                    "startRow":None,
                    "endRow":None
                    })}
            self.client.send(json.dumps(msg), des, "ExceptBreath")



if __name__ == "__main__":
    user = TestUser()
    user.run()
    # a = random_devid(0)

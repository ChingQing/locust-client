import time
import random
import json
import socket
import dubbo_telnet
import requests
from locust import Locust, TaskSet, events, task
# from deviceID import devices_id


class DubboClient(object):
    def __init__(self, host, port):
        self.conn = dubbo_telnet.connect(host, port)
        self.conn.set_connect_timeout(10)

    def do(self,msg):
        start_time = time.time()
        try:
            data= self.conn.do(msg)
            res = json.loads(data)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="dubbo", name="start", response_time=total_time, exception=e)
            
        else:
            if res['code']==0:
                total_time = int((time.time() - start_time) * 1000)
                events.request_success.fire(request_type="dubbo", name="start", response_time=total_time, response_length=0)
            else:
                total_time = int((time.time() - start_time) * 1000)
                events.request_failure.fire(request_type="dubbo", name="start", response_time=total_time, exception="report failed:{}".format(res))

        return data


class DubboLocust(Locust):
    """
    This is the abstract Locust class which should be subclassed. It provides an Stomp client
    that can be used to make Stomp requests that will be tracked in Locust's statistics.
    """
    def __init__(self, *args, **kwargs):
        super(DubboLocust, self).__init__(*args, **kwargs)
        self.client = DubboClient(self.host, self.port)



class TestUser(DubboLocust):

    host = "192.168.1.100"
    port = 20904
    min_wait = 1000
    max_wait = 50000

    class task_set(TaskSet):
        
        @task(1)

        def send_data(self):
            msg = 'invoke com.speak.touch("http://192.168.1.10:2200/FlyH2M3LtAkBtwGYGM7YItsAst7s","",2)'
            data =  self.client.do(msg)



if __name__ == "__main__":
    user = TestUser()
    user.run()


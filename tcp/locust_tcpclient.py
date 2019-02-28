import time
import random
# from socket import socket, AF_INET, SOCK_STREAM
import socket
from locust import Locust, TaskSet, events, task



class TcpSocketClient(socket.socket):
    def connect(self, addr):
        start_time = time.time()
        try:
            super(TcpSocketClient, self).connect(addr)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="tcpsocket", name="connect", response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="tcpsocket", name="connect", response_time=total_time, response_length=0)
        
    def send(self, msg):
        start_time = time.time()
        try:
            super(TcpSocketClient, self).send(msg)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="tcpsocket", name="send", response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="tcpsocket", name="send", response_time=total_time, response_length=0)

    def recv(self, bufsize):
        start_time = time.time()
        try:
            return super(TcpSocketClient, self).recv(bufsize)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="tcpsocket", name="recv", response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="tcpsocket", name="recv", response_time=total_time, response_length=0)

class TcpSocketLocust(Locust):
    """
    This is the abstract Locust class which should be subclassed. It provides an XML-RPC client
    that can be used to make XML-RPC requests that will be tracked in Locust's statistics.
    """
    def __init__(self, *args, **kwargs):
        super(TcpSocketLocust, self).__init__(*args, **kwargs)
        self.client = TcpSocketClient(socket.AF_INET, socket.SOCK_STREAM)

class TcpTestUser(TcpSocketLocust):
    
    host = "127.0.0.1"
    port = 12345
    min_wait = 100
    max_wait = 1000

    class task_set(TaskSet):
        def on_start(self):
            host = "127.0.0.1"
            port = 12345
            ADDR = (host, port)
            print("start client server...")
            self.client.connect(ADDR)

        def on_after(self):
            self.client.close()
        
        @task
        def send_data(self):
            self.client.send(random_str())
            data = self.client.recv(2048).decode()


if __name__ == "__main__":
    user = TcpTestUser()
    user.run()

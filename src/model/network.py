import socket
from ping3 import ping
import time

class NetworkModel:
    def __init__(self):
        self.timeout=2

    def check_ping(self, host):
        try:
            response_time=ping(host, unit="ms", timeout=self.timeout)
            if response_time is None:
                return False, None
            return True, round(response_time, 2)
        except Exception as e:
            return False, str(e)
        
    def check_port(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        try:
            start_time = time.time()  
            result = sock.connect_ex((host, int(port)))
            end_time = time.time()    
            
            if result == 0:
                response_time = round((end_time - start_time) * 1000, 2)
                return True, response_time  
            else:
                return False, 0.0           
        except Exception:
            return False, 0.0              
        finally:
            sock.close()

        


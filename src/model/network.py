import socket
from ping3 import ping

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
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        try:
            result=sock.connect_ex((host, int(port)))
            if result==0:
                return True
            else:
                return False
        except Exception:
            return False
        finally:
            sock.close()

        


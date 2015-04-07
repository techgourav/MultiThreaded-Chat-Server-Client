import socket
import threading

import rendezvous

defaulthost = 'localhost'
port = 50000

class ChatConnect(threading.Thread):
    def __init__(self, host, connected, display, lost):
        threading.Thread.__init__(self)
        self.host = host
        self.connected = connected
        self.display = display
        self.lost = lost
        self.msgLock = threading.Lock()
        self.numMsg = 0
        self.msg = []

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(1)
        try:
            self.socket.connect((self.host, port))
        except:
            self.lost("Unable to connect to %s. Check the server." % self.host)
            return
        self.connected()
        while True:
            self.__send()
            try:
                data = self.socket.recv(4096)
            # Timeout once in a while just to check user input
            except socket.timeout:
                continue
            except:  # server was stopped or had some error
                self.lost("Network Connection closed by the server...")
                break
            if len(data):
                self.display(data)
            else:
                # no data when peer does a socket.close()
                self.lost("Network Connection closed...")
                break
        # End loop of network send / recv data
        self.socket.close()

    def __send(self):
        self.msgLock.acquire()
        if self.numMsg > 0:
            self.socket.send(self.msg.pop(0))
            self.numMsg -= 1
        self.msgLock.release()

    def send(self, msg):
        self.msgLock.acquire()
        self.msg.append(msg)
        self.numMsg += 1
        self.msgLock.release()

import json
import socket
from tkinter import messagebox


class KlijentSock:
    def __init__(self, host=socket.gethostname(), port=12345):
        self.host = host
        self.port = port
        self.s = socket.socket()

    def request(self, poruka):
        response = ""
        try:
            self.s = socket.socket()
            self.s.connect((self.host, self.port))
            self.s.send(json.dumps(poruka).encode())
            response = json.loads(self.s.recv(1024).decode())
        except Exception as exp:
            messagebox.showerror("Greska", "Nije aktivan server!\n%s" % exp)
            self.s.close()
        return response

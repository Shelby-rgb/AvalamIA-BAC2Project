import socket
import json

s = socket.socket()
s.connect((socket.gethostname(), 3001))

matricules = ["18040", "17000"]
port = 3001
name = "La vulcania est toujours la"

msg = {"matricules": matricules,
       "port": port,
       "name": name}

msg = json.dumps(msg)
msg = bytes(msg, "utf-8")

s.send(msg)
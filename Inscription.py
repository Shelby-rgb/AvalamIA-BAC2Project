import socket
import json

s = socket.socket()
s.connect((socket.gethostname(), 3001))

matricules = ["18040", "17051"]
port = 3001
name = "La Vulcania est toujours la"

msg = {"matricules": matricules,
       "port": port,
       "name": name}

msg = json.dumps(msg)
msg = bytes(msg, "utf-8")

s.send(msg)
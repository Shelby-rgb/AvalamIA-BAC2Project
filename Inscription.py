import socket
import json

port = 3001
s = socket.socket()
s.connect((socket.gethostname(), port))

matricules = ["18040", "17051"]
name = "La Vulcania est toujours la"

msg = {"matricules": matricules,
       "port": port,
       "name": name}

msg = json.dumps(msg)
msg = bytes(msg, "utf-8")

s.send(msg)
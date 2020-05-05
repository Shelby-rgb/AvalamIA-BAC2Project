import socket
import json

port = 3001
s = socket.socket()
s.connect((socket.gethostname(), port))

matricules = ["18040", "17051"]
name = "Vulcania est toujours la"

msg = {"matricules": matricules,
       "port": port,
       "name": name}

msg = json.dumps(msg)
msg = bytes(msg, "utf-8")

tot = 0
while tot < len(msg):
       sent = s.send(msg[tot:])
       tot += sent
#s.send(msg)
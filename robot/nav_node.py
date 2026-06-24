import socket
import pickle

UDP_IP = "127.0.0.1"
UDP_PORT = 2055

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
while True:
  data, addr = sock.recvfrom(1024)
  print ("received message:", data)
  line = pickle.loads(data)
  waypoint_x = float(line[0])
  waypoint_y = float(line[1])
  delta = float(line[2])
  print (waypoint_x)
  print (waypoint_y)
  print (delta)

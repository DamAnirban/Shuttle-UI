"""
Simple UDP receiver for debugging/testing the master GUI without a full ROS stack.
Run this on any machine to verify the master is sending packets correctly.
"""
import socket
import pickle

UDP_IP = "127.0.0.1"
UDP_PORT = 2055

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening on {UDP_IP}:{UDP_PORT} ...")

while True:
    data, addr = sock.recvfrom(1024)
    line = pickle.loads(data)
    waypoint_x = float(line[0])
    waypoint_y = float(line[1])
    delta = float(line[2])
    print(f"[{addr[0]}] x={waypoint_x}  y={waypoint_y}  yaw={delta}")

#Author:Jeff Lee
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(('168.0.20.33', 10021))

print('Bound UDP on 10021...')

while True:
    data, addr = s.recvfrom(1024)
    print('Received from %s:%s.' % addr)
    s.sendto(data, addr)


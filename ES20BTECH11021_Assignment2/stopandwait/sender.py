import socket
import time
import os
import math
import struct
import threading

senderIP = "10.0.0.1"
senderPort   = 20001
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize  = 1024 #Message Buffer Size

packet = ""
# Create a UDP socket at reciever side
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
file_name = "testFile.jpg"

not_received = True

time_out = 0.005

def Pack(sq,st):
        packe =struct.pack('!Hs',sq%2,bytes(st,'utf-8'))
        return packe

def send_pack():
    global packet
    global time_out
    global not_received
    global sqn
    while not_received:
        time.sleep(time_out)
        print("timeout happended")
        if not_received:
            socket_udp.sendto(packet, recieverAddressPort)

def rece_pack():
    global ack_data
    global sqn
    global not_received
    global data
    while not_received:
        ack_data = socket_udp.recvfrom(bufferSize)
        if int(ack_data[0]) == sqn%2:
            print(ack_data)
            not_received = False


sqn = 0
ack_data = 1
f=open(file_name,"rb")
file_size = os.path.getsize(file_name)
total_packets = math.ceil(file_size/1021)
while True:
    not_received = True
    print(sqn)
    data = f.read(bufferSize-3)
    if data:
        packet = Pack(sqn,'n')
    else:
        packet = Pack(sqn,'e')
        socket_udp.sendto(packet,recieverAddressPort)
        break
    packet+=data
    socket_udp.sendto(packet, recieverAddressPort)
    #c1 = time.time()
    t1 = threading.Thread(target = send_pack,)
    t2 = threading.Thread(target = rece_pack, )
    #while ack_data != sqn%2:
        #if not t1.is_alive:
    t1.start()
    #if not t2.is_alive:
#    while not_received:
    t2.start()
    t2.join()
    t1.join()
    sqn += 1
f.close()

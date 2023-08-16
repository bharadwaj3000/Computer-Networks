import socket
import time
import os
import math
import struct
import threading
recieverIP = "10.0.0.2"
recieverPort   = 20002
sender_address_port = ("10.0.0.1", 20001)

bufferSize  = 1024
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
socket_udp.bind((recieverIP, recieverPort))

print("UDP socket created successfully....." )
file_dict = {}
f = open("testFile2GBN.jpg",'wb')
def Unpack(packet):
    sq,flag = struct.unpack('!Hs',packet)
    return [sq,flag]

def Pack(sq,st):
        packet =struct.pack('!Hs',0,bytes(st,'utf-8'))
        return packet

last_packet = 200000
i=0



file_size = os.path.getsize("testFile.jpg")
while True:
    if i == 0:
        t_init = time.time()
    data,addr = socket_udp.recvfrom(bufferSize)
    fn = data.strip()
    str1 = data[0:3]
    p = Unpack(str1)

    str2=data[3:]
    if i-1 == last_packet:
        break

    if p[1] == 'e':
         last_packet = int(p[0])
    if(int(p[0]) == i):
        print(i)
        i += 1
        f.write(str2)
        message = str.encode("{}".format(p[0]))
        socket_udp.sendto(message, addr)
    else:
        message = str.encode("{}".format(i-1))
    if i > 1140:
        t_diff = time.time() - t_init
    #print(time.time())
        print(file_size/t_diff)



f.close()
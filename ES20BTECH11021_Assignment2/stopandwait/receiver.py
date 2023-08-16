import socket
import struct
recieverIP = "10.0.0.2"
recieverPort   = 20002

bufferSize  = 1024
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
socket_udp.bind((recieverIP, recieverPort))

print("UDP socket created successfully....." )
file_dict = {}
f = open("testFile2.jpg",'wb')
def Unpack(packet):
    sq,flag = struct.unpack('!Hs',packet)
    return [sq,flag]

def Pack(sq,st):
        packet =struct.pack('!Hs',sq,bytes(st,'utf-8'))
        return packet

i=0
while True:

    data,addr = socket_udp.recvfrom(bufferSize)
    print(i)
    fn = data.strip()
    str1 = data[0:3]
    p = Unpack(str1)
    if(p[1]=='e'):
        break
    else:
        str2=data[3:]
        if(p[0] == i%2):
            i += 1                                                               
            f.write(str2)
        message = str.encode("{}".format(p[0]))
        socket_udp.sendto(message, addr)
f.close()
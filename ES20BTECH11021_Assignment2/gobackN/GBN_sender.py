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

time_out = 0.005
print("Enter the window size: ")
wind = int(input())
f=open(file_name,"rb")
boolean = True

last_packet = 200000

def Pack(sq,st):
		packet =struct.pack('!Hs',sq,bytes(st,'utf-8'))
		return packet



window = {}
counter = 0
while True:
	data = f.read(bufferSize-3)
	if data:
		packet = Pack(counter,'n')
	else:
		packet = Pack(counter,'e')
		break
	packet+=data
	window[counter] = packet
	counter += 1

last_packet = counter

def send_recv():
	global sqn
	global last_packet
	global base
	global boolean
	global nextseqnum
	while boolean:
		while sqn < base+wind:

			#    if data:
			 #       packet = Pack(sqn,'n')
				#else:
				#    packet = Pack(sqn,'e')
					# last_packet = sqn
			#break
			   #packet+=data
			   # window[sqn] = packet
			   # nextseqnum += 1
			socket_udp.sendto(window[sqn], recieverAddressPort)
			timee[sqn] = time.time()

			sqn += 1

def rece_pack():
	global ack_data
	global base
	global boolean
	global sqn
	global last_time
	global last_packet
	while boolean:
		socket_udp.settimeout(0.005)
		try:
			ack_data = socket_udp.recvfrom(bufferSize)
			if int(ack_data[0]) >= base:
				base = int(ack_data[0]) + 1
				last_time = timee[base]
				if int(ack_data[0]) == last_packet:
					boolean = False
		except:
			sqn = base


ack_data = ""
sqn = 0
base = 0
nextseqnum = 0
file_size = os.path.getsize(file_name)
total_packets = math.ceil(file_size/1021)
timee = {}


#t1 = threading.Thread(target = timer,)
t2 = threading.Thread(target=rece_pack,)
t3 = threading.Thread(target = send_recv,)
t3.start()
t2.start()
t2.join()
t3.join()
f.close()
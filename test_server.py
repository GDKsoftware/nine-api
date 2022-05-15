import ctypes
import socket
from libnine import nine_pb2
from libnine.nine_types import msg_type

localIP = "0.0.0.0"
localPort = 20001
bufferSize = 1024

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening to port {}".format(localPort))

buffer = b''

while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    clientIP = bytesAddressPair[1]

    buffer = buffer + message

    if len(buffer) < 8:
        continue

    zerostart = buffer[0]
    msgtype = msg_type(buffer[1])
    chsum = ctypes.c_uint16.from_buffer_copy(buffer[2:4])
    msglen = ctypes.c_uint32.from_buffer_copy(buffer[4:8]).value

    if len(buffer) < 8 + msglen:
        continue

    protobufmessage = buffer[8:8+msglen]
    buffer = buffer[8+msglen+1:]

    if msgtype == msg_type.helloworld:
        hello = nine_pb2.Hello()
        if msglen > 0:
            hello.ParseFromString(protobufmessage)
        print('Discovery from MAC {}, IP + port: {}'.format(hello.identifier, clientIP))
        msgFromServer = "Hello UDP Client"
        bytesToSend = str.encode(msgFromServer)
        UDPServerSocket.sendto(bytesToSend, clientIP)
    elif msgtype == msg_type.onesecond:
        print('Received onesecond')
        onesec = nine_pb2.Onesecond()
        if msglen > 0:
            onesec.ParseFromString(protobufmessage)
        print(onesec)

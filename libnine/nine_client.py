import ctypes
import socket
import string
import subprocess
import re

from libnine import nine_pb2
from libnine.nine_types import msg_type

class nine_client:
    def __init__(self, port: int, broadcastAddress = '192.168.100.255', networkintfname = 'usb0'):
        self.port = port
        self.broadcastAddress = broadcastAddress
        self.discoveredAddress = (self.broadcastAddress, port)
        self.socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.terminated = False
        self.usb0mac = self.get_mac_address(networkintfname)

    def get_mac_address(self, intfname: string):
        macaddr = ''
        output = subprocess.check_output(['ip','-f','link','-o','a'])
        lines = output.decode('utf-8', 'replace')
        for line in lines.splitlines():
            if intfname in line:
                m = re.search('link\/ether\s([0-9a-f:]*)', line)
                macaddr = m.group(1)
        return macaddr

    def discover_server(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.settimeout(2)

        bufferSize = 1024
        while(not self.terminated):
            hello = nine_pb2.Hello()
            hello.identifier = self.usb0mac
            self.send_broadcast(msg_type.helloworld, hello)

            try:
                bytesAddressPair = self.socket.recvfrom(bufferSize)
                address = bytesAddressPair[1]
                self.discoveredAddress = (address[0], self.port)
                break
            except KeyboardInterrupt:
                break
            except:
                continue

        self.reset_socket()

    def stop(self):
        self.terminated = True

    def reset_socket(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 0)
        self.socket.settimeout(None)

    def send_broadcast(self, type: msg_type, msg: any):
        brdcast = (self.broadcastAddress, self.port)
        self.send_to(brdcast, type, msg)

    def send_to(self, addr, type: msg_type, msg: any):
        bytesToSend = msg.SerializeToString()
        zerostart = ctypes.c_uint8(0)
        msglen = ctypes.c_uint32(len(bytesToSend))
        msgtype = ctypes.c_uint8(type.value)
        # todo - figure out a practical checksum
        chsum = ctypes.c_uint16(0)
        self.socket.sendto(bytes(zerostart) + bytes(msgtype) + bytes(chsum) +
                           bytes(msglen) + bytesToSend, addr)

    def send(self, type: msg_type, msg: any):
        self.send_to(self.discoveredAddress, type, msg)

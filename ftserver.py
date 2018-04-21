import socket
import random
from threading import *
import argparse
import datetime
import platform
import os
import string


SERVER_HOST = '0.0.0.0'
SERVER_PORT = 47722
SERVER_ADDR = (SERVER_HOST, SERVER_PORT)

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
connection.bind(SERVER_ADDR)
connection.listen(10)
print('Server started and listening')

client_recv_list = {}


class ft(Thread):
	"""
	This class is used as a Threading object to support concurrency.

	Keyword arguments:
	Thread -- Thread object
	"""

	def __init__(self, client, address):
		"""
		initializer method for Thread

		Keyword arguments:
		self -- class object instance
		client -- socket object for connection
		address -- address bound to the 'client' socket
		"""
		Thread.__init__(self)
		self.sock = client
		self.addr = address
		self.start()

	def run(self):
		"""
		The run, or 'start()' method for the ft class. This starts the Thread
		instance so that the connection can run separately from the main logic.

		Keyword arguments:
		self -- class object reference
		"""
		# For this protocol, the initial connection sends a single bit denoting whether it's 
		# a sender(1) or receiver(0)  
		receiver_bit = self.sock.recv(1)
		
		# If it's a receiver, generate ID and add to dict
		if receiver_bit == b'0':
			ID = random.choice(string.ascii_letters + string.digits)
			while ( ID in client_recv_list ):
				ID = random.choice(string.ascii_letters + string.digits)
			
			# Add receiver entry to dictionary 
			client_recv_list[ID] = self.addr
		else:
			# This is the sender requesting address for a specific ID
			Req_ID = (self.sock.recv(4)).decode()
			if Req_ID in client_recv_list:
				temp = b''
				temp += client_recv_list[Req_ID][0].encode()
				temp += ','.encode()
				temp += str(client_recv_list[Req_ID][1]).encode()
				self.sock.send(temp)
			else:
				self.sock.send(b'0')
		
		print(client_recv_list)
		""" Completed. Shutdown socket"""
		self.sock.shutdown(socket.SHUT_RDWR)
		self.sock.close()
		print("Socket Closed Successfully")

		
########################
########## Main ##########
########################
		
		
while True:
	client, address = connection.accept()
	ft(client, address)

import socket
import random
from threading import *
import argparse
import datetime
import platform
import os
import binascii
import struct
import textwrap
import heapq
import time

mode = None

pq = [] # list of entries arranged in a heap



class ft(Thread):
	"""
	This class is used as a Threading object to support concurrency.

	Keyword arguments:
	Thread -- Thread object
	"""
		## Priority Queue addition
	global pq
	entry_finder = {}               # mapping of blocks to entries
	REMOVED = '<removed-block>'     # placeholder for a removed block
	counter = itertools.count()     # unique sequence count

	def add_block(block, priority=0):
	    'Add a new block or update the priority of an existing block'
	    if block in entry_finder:
	        remove_block(block)
	    count = next(counter)
	    entry = [priority, count, block]
	    entry_finder[block] = entry
	    heappush(pq, entry)

	def remove_block(block):
	    'Mark an existing block as REMOVED.  Raise KeyError if not found.'
	    entry = entry_finder.pop(block)
	    entry[-1] = REMOVED

	def pop_block():
	    'Remove and return the lowest priority block. Raise KeyError if empty.'
	    while pq:
	        priority, count, block = heappop(pq)
	        if block is not REMOVED:
	            del entry_finder[block]
	            return block
	    raise KeyError('pop from an empty priority queue')


	##########################

	def __init__(self, connection, fn, fs):
		"""
		initializer method for Thread

		Keyword arguments:
		self -- class object instance
		client -- socket object for connection
		address -- address bound to the 'client' socket
		"""
		Thread.__init__(self)
		self.conn = connection
		self.fn = fn
		self.fs = fs
		self.start()

	def recv_blocks(client):
		"""
		Used to receive file blocks from the sender and push them to the priority queue

		This function should be threaded
		"""
		global args
		global total_bytes_recvd

		chunks = []
		while True:
			chunk = client.recv(args.size)
			total_bytes_recvd += len(chunk)
			if chunk == b'':
				break
			chunks.append(chunk)
		data = b''.join(chunks)

		block_offset = struct.unpack('I', data[0:4])[0]

		add_block(data[x:], block_offset)

	def run(self):
		"""
		The run, or 'start()' method for the ft class. This starts the Thread
		instance so that the connection can run separately from the main logic.

		This class is for the receiver so it may receive multiple files 
		simultaneously.

		Keyword arguments:
		self -- class object reference
		"""

		print("Receiving \'" + self.fn + "\'...")
		
		total_bytes_recvd = 0
		
		while total_bytes_recvd != self.fs:
			client, address = connection.accept()
			t = Thread(target=recv_blocks, args=(client,))
			t.start()

		newFile = open('./testing/'+self.fn, "wb")
		while True:
			try:
				newFile.write(pop_block)
			except:
				break
			finally:
				newFile.close()

		""" Completed. Shutdown socket"""
		self.sock.shutdown(socket.SHUT_RDWR)
		self.sock.close()
		print("Transfer Complete!")

def get_header(client):
	"""
	Gets the main header for the connection

	returns the header name and total size of the file about to be
	sent.
	"""
	data = client.recv(256)
	
	hex_data = binascii.hexlify(data)
	spaced_hex = ''
	utf_data = hex_data.decode("utf-8")
	spaced_hex = " ".join(utf_data[i:i+2] for i in range(0, len(utf_data), 2))
	data_array = spaced_hex.split()

	hex_name = []
	header_name = ''
	x = 0
	while data_array[x] != "00":
		hex_name.append(data_array[x])
		x += 1
	x += 1
	header_size = int(data_array[x]+data_array[x+1]+data_array[x+2]+data_array[x+3], 16)
	for x in range(0, len(hex_name)):
		header_name += binascii.unhexlify(hex_name[x]).decode("ascii")
	x += 4

	return header_name, file_size

def init_to_server(mode, address, ID):
	
  # Split the HOST:PORT string
  addr_port = address.split(':')
  
  SERVER_HOST = addr_port[0]
  SERVER_PORT = int(addr_port[1])
  SERVER_ADDR = (SERVER_HOST, SERVER_PORT)
  
  ### Sending and recieving byte strings
  connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  connection.connect(SERVER_ADDR)
  print("Asking \'" + addr_port[0] + ":" + addr_port[1] + " about an ID...")

  if mode == 0:
    connection.send(b'0')
    ID = connection.recv(1).decode()
    print("Issued ID for identification...")
    recv_addr = None
    print("ID: " + ID)
  else:
    connection.send(b'1')
    connection.send(b''+ ID.encode())
    recv_addr = connection.recv(256)
  
  connection.close()
  return recv_addr

def run_client(receiver, filename, cons, size):
	
	# Split the HOST:PORT string
  addr_port = address.split(':')

  connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  recv_client = (receiver[0], int(receiver[1]))
  connection.connect(recv_client)

  sendFile = open(filename, "rb")
  temp = sendFile.read()
  CNUM = 4
  offset = (len(temp))/CNUM
  tempsplit = textwrap.wrap(temp, offset)
  print(tempsplit)
  start = 0;
  
 
  print("Sending \'" + filename + "\'...")
  header_string = b''
  header_string += filename.encode()
  header_string += b'\x00'
  start  = offset * i
  header_string += struct.pack("I", len(temp))
  header_string = header_string + temp
  

  totalsent = 0
  while totalsent < len(header_string):
      sent = connection.send(header_string[totalsent:])
      if sent == 0:
          raise RuntimeError("socket connection broken")
      totalsent = totalsent + sent


def run_recv(port, size):
	
	SERVER_HOST = '0.0.0.0'
	SERVER_PORT = int(port)
	SERVER_ADDR = (SERVER_HOST, SERVER_PORT)

	connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	connection.bind(SERVER_ADDR)
	connection.listen(10)
	while True:
		client, address = connection.accept()
		file_name, file_size = get_header(client)
		ft(connection, file_name, file_size)


######################
######## Main ########
######################

parser = argparse.ArgumentParser()
# Stores HOST:PORT in string
parser.add_argument('--server', action='store')

# Indicates receiving client
parser.add_argument('--receive', action='store_true')

# Indicates client and takes in ID FILE
parser.add_argument('--send', nargs = 2)

# Indicates what the client's buffer size should be. (Default 4096) 
parser.add_argument('-s', '--size', default=4096, action='store', type=int)

# Indicates the port that this receiver client will use for it's socket
parser.add_argument('-p','--port', action='store', type=int, default=47695)

# Specifies the number of parallel, concurrent connections to use when sending (default 1)
parser.add_argument('-c', '--cons', default=1, action='store', type=int)
args = parser.parse_args()

address = args.server


if args.receive:
	mode = 0
	temp = init_to_server(mode, address, None)
	run_recv(args.port, args.size)
else:
  	mode = 1
	recv_addr = init_to_server(mode, address, args.send[0])
	receiver = recv_addr.decode("utf-8").split(',')
	print(receiver)
	print("Found client at \'" + receiver[0] + ":" + receiver[1] + "\'...")
	run_client(receiver, args.send[1], args.cons, args.size)

Grant Slone
811414084

Sebastien Nazaire
** Insert 811 number here **

# PJ03

This is a text file transfer protocol that uses a
client-server and client-client connection.

To use this software, start the server:
```
$ python3 ftserver.py [--port PORT]
```

and then start the receiver:
```
$ python3 ftclient.py --server HOST:PORT [-s SIZE] [-p PORT] --receive 
```

This will contact the server and the server will register
the IP of the receiver. It will also print the identifier (0-9/a-x/A-x)
which is a single character. To send the text file, run the client:
```
$ python3 ftclient.py --server HOST:PORT [-c CNUM] [-s SIZE] --send ID FILE 
```

The sending client will terminate when finished. The receiver will not, and 
will remain available to receive until it is terminated with ^C. This is the
same for the server.

Protocol ft is outlined below:

Initial Client-Server handshake exchanges a single bit:
0: Receive
1: Send

The Client-Client protocol is this:
+--------------+
+ filename.txt +
+--------------+
+ size of file +
+--------------+

'Filename' is terminated by a null byte and
'size of file' is 4 bytes. 

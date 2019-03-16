import cv2
import socket
import struct
import argparse
import numpy as np
from pprint import pprint
from knowledge import create_knowledge_graph

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', help='port number for raspberry pi', required=True, type=int)
args = vars(parser.parse_args())

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', args['port']))
server_socket.listen(0)

print("Listening on %d" % args['port'])
connection = server_socket.accept()[0].makefile('rb')
print("Connected to Pi!")

try:
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        raw_bytes = connection.read(image_len)
        image = cv2.imdecode(np.frombuffer(raw_bytes, np.uint8), -1)
        pprint(create_knowledge_graph(image))
finally:
    connection.close()
    server_socket.close()

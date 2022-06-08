import socket
import pickle
import struct


class VideoTx:
    def __init__(self):
        # Socket Create
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Socket Bind
        socket_address = ("0.0.0.0", 9999)
        server_socket.bind(socket_address)

        # Socket Listen
        server_socket.listen(5)
        print("LISTENING AT:", socket_address)
        self.client_socket, addr = server_socket.accept()
        print('GOT CONNECTION FROM:', addr)

    def sendFrame(self, frame):
        a = pickle.dumps(frame)
        message = struct.pack("Q", len(a)) + a
        self.client_socket.sendall(message)

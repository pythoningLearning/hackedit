"""
Contains some utility functions used by both the client and the server.
"""
import logging
import pickle
import socket
import struct


def _logger():
    return logging.getLogger(__name__)


def pick_free_port():
    """ Picks a free port """
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    test_socket.bind(('127.0.0.1', 0))
    free_port = int(test_socket.getsockname()[1])
    test_socket.close()
    return free_port


def read_message(socket):
    """
    Reads a message using our simple protocol (payload + data)
    """
    if not hasattr(socket, 'buffer'):
        socket.buffer = b''
    if not hasattr(socket, 'payload'):
        socket.payload = None
    socket.buffer += socket.readAll()
    if socket.payload is None:
        if len(socket.buffer) >= 8:
            payload = socket.buffer[:8]
            socket.buffer = socket.buffer[8:]
            socket.payload = struct.unpack('Q', payload)[0]
            if len(socket.buffer) >= socket.payload:
                return pickle.loads(socket.buffer)
    return None  # message not complete, let's wait for other packets


def send_message(socket, data):
    """
    Sends a message using our rudimentary protocol.
    """
    data = pickle.dumps(data)
    payload = struct.pack('Q', len(data))
    socket.write(payload + data)
    socket.flush()
    data = None
    del data


def echo(*args):
    print('function called in a subprocess with args=', args)

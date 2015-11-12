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
    if not hasattr(socket, '_buffer'):
        socket._buffer = b''
    if not hasattr(socket, '_payload'):
        socket._payload = None
    socket._buffer += socket.readAll()
    results = None
    while socket._buffer:
        if socket._payload is None:
            if len(socket._buffer) >= 8:
                payload = socket._buffer[:8]
                socket._buffer = socket._buffer[8:]
                socket._payload = struct.unpack('Q', payload)[0]
            else:
                # payload buffer not complete, let's wait for another
                # packet
                return None
        else:
            # read data
            if len(socket._buffer) >= socket._payload:
                results = pickle.loads(socket._buffer)
                del socket._buffer
                del socket._payload
                socket.close()
                socket.deleteLater()
            else:
                # data buffer not complete, let's wait for another packet
                pass

        return results


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

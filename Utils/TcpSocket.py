from socket import socket, error, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from struct import pack, unpack, calcsize

class TcpSocket(object):

    def __init__(self, accepted=None):
        if not accepted:
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.sock = accepted

    def close(self):
        self.sock.close()

    def client(self, host):
        self.sock.connect(host)
        return self

    def server(self, host):
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind(host)
        self.sock.listen(5)
        return self

    def accept(self):
        sock, addr = self.sock.accept()
        return TcpSocket(accepted=sock), addr

    def send(self, content):
        frame = self._make_frame(content)
        self.sock.sendall(frame)

    def recv(self):
        header = self._recv(calcsize('>i'))
        content_size = unpack('>i', header)[0]
        content = self._recv(content_size)
        return content

    def send_utf8(self, content):
        self.send(content.encode('utf-8'))

    def recv_utf8(self):
        return self.recv().decode('utf-8')

    def send_ascii(self, content):
        self.send(content.encode('ascii'))

    def recv_ascii(self):
        return self.recv().decode('ascii')

    def _make_frame(self, content):
        content_size = pack('>i', len(content))
        frame = content_size + content
        return frame

    def _recv(self, size):
        chunk = bytes()
        while len(chunk) < size:
            part = self.sock.recv(size - len(chunk))
            if not part:
                raise error('Empty Socket')
            chunk += part
        return chunk

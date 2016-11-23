import pytest
from Utils.TcpSocket import *

class TestTcpSocket(object):
    
    def test_client(self, mocker):
        args = (('localhost', 5000), )
        connect_args = (('localhost', 5000), )
        connect = mocker.patch('Utils.TcpSocket.socket.connect')
        TcpSocket().client(*args)
        connect.assert_called_once_with(*connect_args)

    def test_client_failure(self):
        with pytest.raises(error) as err:
            TcpSocket().client(('localhost', 5000))
        assert '111' in str(err.value)

    def test_server(self, mocker):
        args = (('', 5000), )
        setsockopt_args = (SOL_SOCKET, SO_REUSEADDR, 1)
        bind_args = (('', 5000), )
        listen_args = (5, )
        setsockopt = mocker.patch('Utils.TcpSocket.socket.setsockopt')
        bind = mocker.patch('Utils.TcpSocket.socket.bind')
        listen = mocker.patch('Utils.TcpSocket.socket.listen')
        TcpSocket().server(*args)
        setsockopt.assert_called_once_with(*setsockopt_args)
        bind.assert_called_once_with(*bind_args)
        listen.assert_called_once_with(*listen_args)

    def test_server_accept(self, mocker):
        expected_sock = socket(AF_INET, SOCK_STREAM)
        expected_addr = '127.0.0.1:29800'
        accept = mocker.patch('Utils.TcpSocket.socket.accept')
        accept.return_value = (expected_sock, expected_addr)
        sock, addr = TcpSocket().accept()
        assert addr == expected_addr
        assert type(sock) is TcpSocket
        assert sock.sock is expected_sock

    def test_close(self, mocker):
        close = mocker.patch('Utils.TcpSocket.socket.close')
        TcpSocket().close()
        assert close.called == True

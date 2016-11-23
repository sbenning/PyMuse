from MuseGlobal import MuseTable, Paths, IP_SERVER, COM_PORT, CMD_PORT
from Utils.TcpSocket import TcpSocket, error
from Utils.Osc import OscPath
from Subscribers import Subscribers
from threading import Thread

def start_thread(handler, *args):
    thread = Thread(target=handler, args=args)
    thread.daemon = True
    thread.start()       

def dispatch(clients, frame):
    path = OscPath(frame).path
    if not path in Paths:
        return
    key = Paths[path]
    for tcp in clients.get_subscribers(key):
        tcp.send(frame)

def com_handler(clients):
    tcp = TcpSocket().server((IP_SERVER, COM_PORT))
    io_tcp, addr = tcp.accept()
    print('Connection MuseIO', addr)
    while 42:
        try:
            frame = io_tcp.recv()
        except error as err:
            print(err)
            break
        dispatch(clients, frame)
    io_tcp.close()
    print('Com Handler Stop')

def client_handler(client):
    print('Connection Client', client.addr)
    while 42:
        try:
            key = int(client.tcp.recv_ascii())
        except error as err:
            break
        if key not in MuseTable:
            break
        client.subscribe_toggle(key)
    client.kill()
    print('Client Handler Stop', client.addr)
 
def cmd_handler(clients):
    tcp = TcpSocket().server((IP_SERVER, CMD_PORT))
    while 42:
        client_tcp, addr = tcp.accept()
        start_thread(client_handler, clients.add((client_tcp, addr)))

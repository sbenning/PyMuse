from MuseGlobal import MuseTable, Name
from Utils.TcpSocket import TcpSocket, error
from MuseMsg import MuseMsg
from threading import Thread
from time import sleep

class MuseData(object):

    def update(self, frame):
        msg = MuseMsg(frame)
        self.__dict__.update({Name(msg.path) : msg.args})


class Muse(object):
    def __init__(self, host):
        self.data = MuseData()
        self._data = MuseData()
        self._tcp = TcpSocket().client(host)
        self._start_thread()

    def subscribe(self, key):
        self._subscribe_toggle(key)
        self._wait(Name(MuseTable[key]['path']))

    def unsubscribe(self, key):
        self._subscribe_toggle(key)

    def update(self):
        self.data.__dict__.update(self._data.__dict__)

    def stop(self):
        self._subscribe_toggle(-1)
        self._tcp.close()

    def _subscribe_toggle(self, key):
        self._tcp.send_ascii(str(key))

    def _wait(self, name):
        while not name in self.data.__dict__:
            self.update()
            sleep(0.02)

    def _start_thread(self):
        producer = Thread(target=self._producer)
        producer.daemon = True
        producer.start()

    def _producer(self):
        while 42:
            try:
                frame = self._tcp.recv()
            except error as err:
                break
            self._data.update(frame)

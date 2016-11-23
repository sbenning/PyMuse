class Subscriber(object):

    def __init__(self, host):
        self.tcp, self.addr = host
        self.keys = set()

    def subscribe_toggle(self, key):
        if key in self.keys:
            self.keys.remove(key)
        else:
            self.keys.add(key)

    def kill(self):
        self.keys = set()
        self.tcp.close()

class Subscribers(object):

    def __init__(self):
        self.subscribers = dict()

    def get_subscribers(self, key):
        for subscriber in self.subscribers.items():
            if key in subscriber.keys:
                yield subscriber.tcp

    def add(self, host):
        subscriber = Subscriber(host)
        self.subscribers.update({subscriber.addr : subscriber})
        return subscriber

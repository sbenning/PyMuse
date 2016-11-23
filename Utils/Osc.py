from math import ceil
from struct import unpack

class OscError(Exception):
    pass


def _osc_round_len(length):
    return int(ceil((length / 4.0)) * 4)

def _osc_readstring(frame):
    length = frame.find(b'\0')
    if not frame or length < 0:
        raise OscError('OscError : Invalid string syntax for : ' + repr(frame))
    return frame[:length].decode('utf-8'), frame[_osc_round_len(length + 1):]

def _osc_readint(frame):
    if len(frame) < 4:
        raise OscError('OscError : Invalid int syntax for : ' + repr(frame))
    return unpack('>i', frame[:4])[0], frame[4:]

def _osc_readfloat(frame):
    if len(frame) < 4:
        raise OscError('OscError : Invalid float syntax for : ' + repr(frame))
    return unpack('>f', frame[:4])[0], frame[4:]

PARSE = {
        's' : _osc_readstring,
        'i' : _osc_readint,
        'f' : _osc_readfloat
        }

class OscMsg(object):
    def __init__(self, frame):
        if not frame or type(frame) != bytes:
            raise OscError('OscError : Invalid frame for : ' + repr(frame))
        self.frame = frame
        self.path, frame_rest = self._osc_read_path(frame)
        self.typetag, frame_rest = self._osc_read_typetag(frame_rest)
        self.args = []
        for c in self.typetag:
            arg, frame_rest = PARSE[c](frame_rest)
            self.args.append(arg)

    def _osc_read_path(self, frame):
        try:
            path, frame_rest = _osc_readstring(frame)
        except OscError:
            raise OscError('OscError : Invalid frame path for : ' + repr(frame))
        if not path:
            raise OscError('OscError : Invalid frame path for : ' + repr(frame))
        return path, frame_rest

    def _osc_read_typetag(self, frame):
        try:
            typetag, frame_rest = _osc_readstring(frame)
        except OscError:
            raise OscError('OscError : Invalid frame typetag for : ' + repr(frame))
        if not typetag or typetag[0] != ',':
            raise OscError('OscError : Invalid frame typetag for : ' + repr(frame))
        else:
            typetag = typetag[1:]
        if any(c for c in typetag if c not in PARSE) or not frame_rest:
            raise OscError('OscError : Invalid frame typetag for : ' + repr(frame))
        return typetag, frame_rest


class OscPath(OscMsg):
    def __init__(self, frame):
        if not frame or type(frame) != bytes:
            raise OscError('OscError : Invalid frame for : ' + repr(frame))
        self.frame = frame
        self.path, frame_rest = self._osc_read_path(frame)

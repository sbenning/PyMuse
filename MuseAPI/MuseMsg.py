from Utils.Osc import OscMsg
from MuseGlobal import Paths

class MuseMsg(OscMsg):

    def __init__(self, frame):
        OscMsg.__init__(self, frame)
        self.key = Path[self.path]

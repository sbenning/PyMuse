from MuseGlobal import IP, CLI_PORT, IS_GOOD, BLINK
from MuseAPI import Muse
from time import time, sleep

def main():
    try:
        muse = Muse((IP, CLI_PORT))
    except Exception as err:
        print(err)
        return
    muse.subscribe(IS_GOOD)
    muse.subscribe(BLINK)
    now = time()
    while time() < now + 42:
        print(muse.data.is_good, muse.data.blink)
        muse.update()
    muse.stop()

if __name__ == '__main__':
    main()

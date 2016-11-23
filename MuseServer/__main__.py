from MuseServer import Subscribers, com_handler, cmd_handler, start_thread

def main():
    clients = Subscribers()
    start_thread(com_handler, clients)
    start_thread(cmd_handler, clients)
    input('Press Enter to Quit\n')

if __name__ == '__main__':
    main()

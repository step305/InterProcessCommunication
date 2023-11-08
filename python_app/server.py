import socket
from threading import Thread
import queue
import select

TCP_IP = 'localhost'
TCP_PORT = 60001
BUFFER_SIZE = 1024


class ClientThread(Thread):
    def __init__(self, ip_, port_, sock_, data_queue_, command_queue_, quit_flag_):
        Thread.__init__(self)
        self.ip = ip_
        self.port = port_
        self.sock = sock_
        self.data = data_queue_
        self.commands = command_queue_
        self.quit_flag = quit_flag_
        self.sock.setblocking(0)
        print(" New thread started for " + ip_ + ":" + str(port_))

    def run(self):
        buffer = ''
        while True:
            if self.quit_flag.is_set():
                self.sock.close()
                break
            try:
                message = self.data.get(block=False)
                print('send to client:', str(message))
                self.sock.send((str(message) + '$').encode('utf-8'))
                ready = True
                while ready:
                    ready = select.select([self.sock], [], [], 0.01)
                    if ready[0]:
                        x = self.sock.recv(1).decode('utf-8')
                        if x != '$':
                            buffer += x
                        else:
                            print('command from client:', buffer)
                            self.commands.put(buffer)
                            buffer = ''
                    else:
                        ready = False
            except queue.Empty:
                continue
            except Exception:
                break


def server_proc(data_queue, command_queue, quit_flag):
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpsock.bind((TCP_IP, TCP_PORT))
    threads = []
    tcpsock.settimeout(1)
    print("Waiting for incoming connections...")

    while not quit_flag.is_set():
        try:
            tcpsock.listen(1)
            (conn, (ip, port)) = tcpsock.accept()
            print('Got connection from ', (ip, port))
            new_thread = ClientThread(ip, port, conn, data_queue, command_queue, quit_flag)
            new_thread.start()
            threads.append(new_thread)
        except:
            pass

    for t in threads:
        t.join()

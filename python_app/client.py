import socket
import time

TCP_IP = 'localhost'
TCP_PORT = 60001

BUFFER_SIZE = 1024


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((TCP_IP, TCP_PORT))
    buffer = ''
    t0 = time.time()

    while True:
        try:
            data = s.recv(1024)
            for i in range(len(data)):
                x = data[i:i+1].decode('utf-8')
                if x != '$':
                    buffer += x
                else:
                    print(buffer)
                    buffer = ''
            if not data:
                break
            if time.time() - t0 > 5.0:
                t0 = time.time()
                s.send('next_command$'.encode('utf-8'))
        except KeyboardInterrupt:
            break
    s.close()


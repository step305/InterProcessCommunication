import queue
import time
import subprocess
import json
import threading
import server


def cpp_read_proc(out_queue, in_queue, quit_flag):
    cpp_proc = subprocess.Popen(
        '../Cpp_app/cmake-build-debug/Cpp_app.exe',
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    while not quit_flag.is_set():
        try:
            message = cpp_proc.stdout.readline()
            data = json.loads(message.decode('utf-8'))
            out_queue.put(data)
            try:
                command = in_queue.get(block=False)
                cpp_proc.stdin.write('{}\r\n'.format(command).encode('utf-8'))
                cpp_proc.stdin.flush()
            except queue.Empty:
                pass
        except Exception as e:
            print(e)
            break
    cpp_proc.kill()
    print('Exiting')


if __name__ == '__main__':
    cpp_command_queue = queue.Queue()
    cpp_data_queue = queue.Queue()
    cpp_quit_flag = threading.Event()
    t0 = time.time()

    cpp_thread = threading.Thread(target=cpp_read_proc, args=(cpp_data_queue, cpp_command_queue, cpp_quit_flag,))
    cpp_thread.start()
    server_thread = threading.Thread(target=server.server_proc, args=(cpp_data_queue, cpp_command_queue, cpp_quit_flag,))
    server_thread.start()

    while True:
        try:
            pass
        except KeyboardInterrupt:
            break
    cpp_quit_flag.set()
    cpp_thread.join()
    server_thread.join()
    print('Done!')

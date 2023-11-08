#include <iostream>
#include <csignal>
#include <unistd.h>
#include<thread>
#include <atomic>
#include <mutex>

std::mutex command_mutex;
std::string command;
std::atomic_bool command_ready(false);
std::atomic_bool command_quit(false);
std::thread command_thread;

void read_command() {
    while (! command_quit) {
        std::string tmp;
        std::cin >> tmp;
        auto lock = std::unique_lock<std::mutex>(command_mutex);
        command = tmp;
        command_ready = true;
        lock.unlock();
    }
    std::cout << "exiting" << std::endl;
}

void exit_handler(int s){
    command_quit = true;
    if (command_thread.joinable()) {
        command_thread.join();
    }
    printf("Caught signal %d. Exiting\n",s);
    exit(1);
}

int main() {
    signal (SIGINT, exit_handler);
    command = "";

    long cnt = 0;
    double a = 3.1415926;

    command_thread = std::thread(read_command);

    while (true) {
        std::cout << "{\"cnt\": " << cnt << ", \"data\": " << a << ", \"command\": \"\"}" << std::endl;
        std::cout.flush();
        if (command_ready) {
            auto lock = std::unique_lock<std::mutex>(command_mutex);
            std::string last_command = command;
            command_ready = false;
            lock.unlock();
            std::cout << "{\"cnt\": " << cnt << ", \"data\": " << a * 2 << ", \"command\": \"" << last_command << "\"}" << std::endl;
            std::cout.flush();
        }
        cnt++;
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    }
    return 0;
}

cmake_minimum_required(VERSION 3.21)
project(Cpp_app)

set(CMAKE_CXX_STANDARD 20)
find_package (Threads REQUIRED)

add_executable(
        Cpp_app main.cpp
        ${CMAKE_THREAD_LIBS_INIT}
        )

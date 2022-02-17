cmake_minimum_required(VERSION 3.21)
project(fel)

set(CMAKE_CXX_STANDARD 14)

add_executable(fel main.cpp)
add_executable(fel_hw00 hw00.c)
add_executable(fel_hw00-in-out in_out.c)
add_executable(fel_std_out_err std_out_err.c)
add_executable(fel_std_in std_in.c)

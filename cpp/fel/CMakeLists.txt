cmake_minimum_required(VERSION 3.16)
project(fel)
set(CMAKE_CXX_STANDARD 14)
add_executable(fel
        C_programming/projects/02/loan.c C_programming/projects/03/dates.c C_programming/projects/03/products.c C_programming/projects/03/books.c)

project(queue)
set(CMAKE_CXX_STANDARD 14)
add_executable(queue
        HW06/b3b36prg-hw06/queue.h HW06/b3b36prg-hw06/queue.c HW06/b3b36prg-hw06/main.c)

project(cprog)
set(CMAKE_CXX_STANDARD 14)
add_executable(cprog
        C_programming/projects/03/books.h
        C_programming/projects/03/books.c
        C_programming/projects/main.c)


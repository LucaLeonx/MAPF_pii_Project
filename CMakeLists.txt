cmake_minimum_required(VERSION 3.5)
project(MAPF_Bench)
#add_subdirectory(source)
add_executable(mapfBench
        source/main.cpp
        source/Answer.cpp
        source/Answer.h)

add_subdirectory(test)

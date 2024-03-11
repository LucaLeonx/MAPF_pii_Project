include(FetchContent)

FetchContent_Declare(
        Catch2
        GIT_REPOSITORY https://github.com/catchorg/Catch2.git
        GIT_TAG        v3.4.0 # or a later release
)

FetchContent_MakeAvailable(Catch2)

find_package(Catch2 3 REQUIRED)

add_executable(testing answer.cpp
        ../source/Graph.cpp
        ../source/Graph.h
        ../source/Node.cpp
        ../source/Node.h)
target_link_libraries(testing PRIVATE Catch2::Catch2WithMain)

include(Catch)
catch_discover_tests(testing)
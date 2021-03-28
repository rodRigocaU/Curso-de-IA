cmake_minimum_required(VERSION 3.15)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

project(PathFinderG)

find_package(SFML COMPONENTS system window graphics REQUIRED)

file(GLOB SOURCES
    src/*.cpp
    include/*.h
)

include_directories(include data)

add_executable(${PROJECT_NAME} ${SOURCES})

if (SFML_FOUND)
    target_link_libraries(${PROJECT_NAME}
        sfml-graphics
        sfml-window
        sfml-system
    )
    if (WIN32)
        file(GLOB BINARY_DEP_DLLS "${SFML_DIR}/../../../bin/*.dll")
        file(COPY ${BINARY_DEP_DLLS} DESTINATION ${CMAKE_BINARY_DIR})    
    endif()
endif()
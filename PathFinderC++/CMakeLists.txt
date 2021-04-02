cmake_minimum_required(VERSION 3.15)

set(CMAKE_CXX_STANDARD 17)

project(PathFinder)

find_package(SFML COMPONENTS system window graphics REQUIRED)

file(GLOB SOURCES
    src/*.cpp
    include/*.h
)

add_executable(${PROJECT_NAME} ${SOURCES})

include_directories("${CMAKE_CURRENT_SOURCE_DIR}/src")

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
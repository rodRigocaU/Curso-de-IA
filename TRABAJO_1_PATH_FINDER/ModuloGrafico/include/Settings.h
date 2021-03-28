#ifndef SETTINGS_H_
#define SETTINGS_H_

#include <fstream>
#include <iostream>
#include <SFML/Graphics.hpp>

#define WINDOW_SIZE_W     500
#define WINDOW_SIZE_H     650
#define WINDOW_TITLE      "Path Finder Algorithms"

#define CELL_ST_VISITED   1
#define CELL_ST_NVISITED  2
#define CELL_WRONG_WAY    3//cells out of the result path
#define CELL_GOOD_WAY     4//cells in the result path
#define CELL_BLOCKED      0

#define VIEW_MODE_GRAPH   1
#define VIEW_MODE_BOXES   0

#define MOVE_CAMERA_LEFT  A
#define MOVE_CAMERA_RIGHT D
#define MOVE_CAMERA_TOP   W
#define MOVE_CAMERA_DOWN  S
#define CAMERA_ZOOM_CLOSE E
#define CAMERA_ZOOM_FAR   Q
#define KEYBOARD(id_key) sf::Keyboard::id_key

#endif//SETTINGS_H_
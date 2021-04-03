#ifndef SETTINGS_H_
#define SETTINGS_H_

#define WINDOW_SIZE_W       750
#define WINDOW_SIZE_H       750
#define WINDOW_TITLE        "Path Finder Algorithms"
#define VERTICAL_SYNC       1

#define CELL_SIZE           20
#define DEFAULT_SPARCING    4

#define SET_MODE_NONE       -1
#define SET_MODE_BEGIN_CELL 1
#define SET_MODE_END_CELL   2
#define SET_MODE_OBSTACLE   3
#define SET_MODE_NORMAL     4
//Keys Graph Configuration:
#define KEY_BEGIN_CELL      B
#define KEY_END_CELL        N
#define KEY_PUT_OBSTACLE    O
#define KEY_REM_OBSTACLE    I
#define KEY_RESET_GRAPH     R
//----
#define ID_A_STAR           0
#define ID_BFS              1
#define ID_DFS              2
#define ALG_LIMIT           3
//Keys Algorithm:
#define KEY_RUN_ALGORITHM   P
#define KEY_CLEAR_VISITED   L
#define KEY_NEXT_ALGORITHM  Right
#define KEY_PREV_ALGORITHM  Left
//----
//Keys Camera:
#define MOVE_CAMERA_LEFT    A
#define MOVE_CAMERA_RIGHT   D
#define MOVE_CAMERA_TOP     W
#define MOVE_CAMERA_DOWN    S
#define CAMERA_ZOOM_CLOSE   E
#define CAMERA_ZOOM_FAR     Q
//----
#define KEYBOARD(id_key)    sf::Keyboard::isKeyPressed(sf::Keyboard::id_key)

#define CAMERA_X_VEL        2.5
#define CAMERA_Y_VEL        2.5
#define CAMERA_ZOOMFACM     1.02
#define CAMERA_ZOOMFACP     0.95
#define CAMERA_MOVE_FAC     0.006

#define INFINITY_FLOAT      99999.0

#endif//SETTINGS_H_
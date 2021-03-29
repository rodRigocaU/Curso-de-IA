#ifndef SETTINGS_H_
#define SETTINGS_H_

#define WINDOW_SIZE_W     660
#define WINDOW_SIZE_H     680
#define WINDOW_TITLE      "Path Finder Algorithms"

#define CELL_SIZE         15

#define CELL_BEGIN        '1'
#define CELL_END          '2'
#define CELL_ST_VISITED   '3'
#define CELL_ST_NVISITED  '4'
#define CELL_WRONG_WAY    '5'//cells out of the result path
#define CELL_GOOD_WAY     '6'//cells in the result path
#define CELL_BLOCKED      '0'

#define VIEW_MODE_GRAPH   1
#define VIEW_MODE_BOXES   0

#define CAMERA_X_VEL      2.5
#define CAMERA_Y_VEL      2.5
#define CAMERA_ZOOMFACM   1.02
#define CAMERA_ZOOMFACP   0.95
#define CAMERA_MOVE_FAC   0.006

#define MOVE_CAMERA_LEFT  A
#define MOVE_CAMERA_RIGHT D
#define MOVE_CAMERA_TOP   W
#define MOVE_CAMERA_DOWN  S
#define CAMERA_ZOOM_CLOSE E
#define CAMERA_ZOOM_FAR   Q
#define KEY_MODE_GRAPH    G
#define KEY_MODE_BOXES    B
#define KEY_FORWARD_PL    Right
#define KEY_BACKWARD_PL   Left
#define KEYBOARD(id_key)  sf::Keyboard::isKeyPressed(sf::Keyboard::id_key)

#endif//SETTINGS_H_
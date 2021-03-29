#include "PFA_Tools.h"

int main(){
  sf::RenderWindow window(sf::VideoMode(WINDOW_SIZE_W, WINDOW_SIZE_H), WINDOW_TITLE);
  sf::Event action;
  sf::View camera2d = window.getDefaultView();
  view_mode = VIEW_MODE_BOXES;
  window.setFramerateLimit(60);
  std::vector<AlgorithmState> playlist;
  playlist.resize(1);
  algstate_idx = 0;

//example: test camera
  sf::CircleShape circle(50,10);
  circle.setFillColor(sf::Color::Magenta);
//--

  while (window.isOpen()){
    while(window.pollEvent(action)){
      if(action.type == sf::Event::Closed)
        window.close();
      if(action.type == sf::Event::KeyPressed){
        onViewModeControl();
      }
    }
    onCameraControl(camera2d);
    onPlaylistControl(playlist);
    window.clear(sf::Color::White);

    window.setView(camera2d);
//example
    window.draw(circle);
//--
    drawGrid(window, playlist[algstate_idx]);

    window.display();
  }
  
  
  return 0;
}
#include "PFA_Tools.h"

int main(){
  std::vector<AlgorithmState> playlist;

  readPlaylist(playlist);

  sf::RenderWindow window(sf::VideoMode(WINDOW_SIZE_W, WINDOW_SIZE_H), WINDOW_TITLE);
  window.setVerticalSyncEnabled(1);//en true arregla los errores de renderizado.
  sf::Event action;
  sf::View camera2d = window.getDefaultView();
  sf::Vector2<float> center(playlist[0][0].size()*CELL_SIZE, playlist[0].size()*CELL_SIZE);
  std::cout << "Grid size: " << center.x << ' ' << center.y << std::endl;
  camera2d.setCenter(0.5f*center);
  view_mode = VIEW_MODE_BOXES;
  window.setFramerateLimit(60);

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

    drawGrid(window, playlist[algstate_idx]);

    window.display();
  }
  
  
  return 0;
}
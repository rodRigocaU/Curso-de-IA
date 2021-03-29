#include "PFA_Tools.h"

bool readData(const std::string& filename, std::vector<AlgorithmState>& playlist){
  std::ifstream source_file;
  source_file.open(filename);
  if(source_file.is_open()){
    AlgorithmState new_state;
    char cell_state;
    new_state.resize(1);
    while(true){
      source_file.get(cell_state);
      if(source_file.eof())
        break;
      if(cell_state == '\n')
        new_state.resize(new_state.size() + 1);
      else
        new_state[new_state.size() - 1].push_back(cell_state);
    }
    playlist.push_back(new_state);
    source_file.close();
    std::cout << "\nFile " << filename << " done.\n";
    remove(filename.c_str());//comentar si no quieres que los archivos se eliminen luego de su uso
    return true;
  }
  return false;
}

void readPlaylist(std::vector<AlgorithmState>& playlist){
  algstate_idx = 0;
  uint32_t file_counter = 0;
  while(true){
    try{
      if(!readData("data/"+std::to_string(++file_counter)+".txt", playlist))
        throw file_counter - 1;
    }catch(const uint32_t& readed_files){
      if(readed_files == 0) {
        std::cerr << "Data folder is empty." << std::endl;
        exit(EXIT_FAILURE);
      }
      std::cout << "Number of states: " << readed_files << std::endl;
      break;
    }
  }
}

void drawCell(sf::RenderWindow& window, const uint32_t& x, const uint32_t& y, const char& cell){
  sf::RectangleShape cell_d(sf::Vector2f(CELL_SIZE, CELL_SIZE));
  cell_d.setPosition(y*CELL_SIZE,x*CELL_SIZE);
  cell_d.setOutlineColor(sf::Color::Black);
  cell_d.setOutlineThickness(1.5);
  switch(cell){
    case CELL_BEGIN:
      cell_d.setFillColor(sf::Color::Green);
      break;
    case CELL_END:
      cell_d.setFillColor(sf::Color::Magenta);
      break;
    case CELL_ST_VISITED:
      cell_d.setFillColor(sf::Color::Yellow);
      break;
    case CELL_ST_NVISITED:
      cell_d.setFillColor(sf::Color(240,240,240));
      break;
    case CELL_WRONG_WAY:
      cell_d.setFillColor(sf::Color::Red);
      break;
    case CELL_GOOD_WAY:
      cell_d.setFillColor(sf::Color(10,205,10));
      break;
    case CELL_BLOCKED:
      cell_d.setFillColor(sf::Color::Blue);
      break;
  }
  window.draw(cell_d);
}

void drawGrid(sf::RenderWindow& window, std::vector<AlgorithmState>& playlist){
  AlgorithmState* algstate = &playlist[algstate_idx];
  for(std::size_t x = 0; x < algstate->size(); ++x){
    for(std::size_t y = 0; y < (*algstate)[x].size(); ++y){
      drawCell(window, x, y, (*algstate)[x][y]);
    }
  }
}

void onCameraControl(sf::View& camera){
  double size = camera.getSize().x*CAMERA_MOVE_FAC;
  if(KEYBOARD(MOVE_CAMERA_LEFT))
    camera.move(-CAMERA_X_VEL*size, 0);
  if(KEYBOARD(MOVE_CAMERA_RIGHT))
    camera.move(+CAMERA_X_VEL*size, 0);
  if(KEYBOARD(MOVE_CAMERA_TOP))
    camera.move(0, -CAMERA_Y_VEL*size);
  if(KEYBOARD(MOVE_CAMERA_DOWN))
    camera.move(0, +CAMERA_Y_VEL*size);
  if(KEYBOARD(CAMERA_ZOOM_CLOSE))
    camera.zoom(CAMERA_ZOOMFACP);
  if(KEYBOARD(CAMERA_ZOOM_FAR))
    camera.zoom(CAMERA_ZOOMFACM);
}

void onPlaylistControl(std::vector<AlgorithmState>& playlist){
  if(KEYBOARD(KEY_FORWARD_PL)){
    if(++algstate_idx == playlist.size())
      algstate_idx = 0;
    std::cout << "Update play list index: " << algstate_idx << std::endl;
  }
  if(KEYBOARD(KEY_BACKWARD_PL)){
    if(--algstate_idx < 0)
      algstate_idx = playlist.size() - 1;
    std::cout << "Update play list index: " << algstate_idx << std::endl;
  }
}

void onViewModeControl(){
  if(KEYBOARD(KEY_MODE_BOXES)){
    view_mode = VIEW_MODE_BOXES;
    std::cout << "Update view mode: BOXES" << std::endl;
  }
  if(KEYBOARD(KEY_MODE_GRAPH)){
    view_mode = VIEW_MODE_GRAPH;
    std::cout << "Update view mode: GRAPH" << std::endl;
  }
}
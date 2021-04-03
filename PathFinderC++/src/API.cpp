#include "../include/API.h"

sf::Color makeDarkness(const sf::Color& color){
  sf::Color darkcolor;
  darkcolor.r = ((color.r - 60 < 0)?0:(color.r - 60)) % 255;
  darkcolor.g = ((color.g - 60 < 0)?0:(color.g - 60)) % 255;
  darkcolor.b = ((color.b - 60 < 0)?0:(color.b - 60)) % 255;
  return darkcolor;
}

void PathFinder::printCurrentAlgorithm(){
  if(id_algorithm == ID_A_STAR)
    std::cout << "Status: ALGORITHM A*\n";
  if(id_algorithm == ID_BFS)
    std::cout << "Status: ALGORITHM BFS\n";
  if(id_algorithm == ID_DFS)
    std::cout << "Status: ALGORITHM DFS\n";
}

PathFinder::PathFinder(){
  std::cout << "Width: "; std::cin >> size_w;
  std::cout << "Height: "; std::cin >> size_h;
  app = std::make_unique<sf::RenderWindow>(sf::VideoMode(WINDOW_SIZE_W,WINDOW_SIZE_H), WINDOW_TITLE);
  app->setVerticalSyncEnabled(VERTICAL_SYNC);
  camera = app->getDefaultView();
  sparcing = CELL_SIZE;
  nbegin = nullptr;
  nend = nullptr;
  set_mode_status = SET_MODE_NONE;
  id_algorithm = 0;
  printCurrentAlgorithm();
}

void PathFinder::resetGraph(){
  nbegin = nend = nullptr;
  for(std::vector<Node>& line : nodes){
    for(Node& node : line){
      node.isVisited = false;
      node.isObstacle = false;
      node.isBegin = false;
      node.isEnd = false;
      node.local_distance_from_begin = node.global_distance_to_end = INFINITY_FLOAT;
      node.parent = nullptr;
    }
  }
}

void PathFinder::clearVisited(){
  for(std::vector<Node>& line : nodes){
    for(Node& node : line){
      node.isVisited = false;
      node.parent = nullptr;
      node.local_distance_from_begin = node.global_distance_to_end = INFINITY_FLOAT;
    }
  }
}

void PathFinder::showGraph(){
  sf::RectangleShape rect(sf::Vector2f(sparcing,sparcing));
  rect.setOutlineThickness(-DEFAULT_SPARCING);
  for(std::vector<Node>& line : nodes){
    for(Node& node : line){
      rect.setPosition(node.x * sparcing, node.y * sparcing);
      if(node.isObstacle)
        rect.setFillColor(sf::Color::Magenta);
      else if(node.isBegin)
        rect.setFillColor(sf::Color::Green);
      else if(node.isEnd)
        rect.setFillColor(sf::Color::Red);
      else if(node.isVisited)
        rect.setFillColor(sf::Color(100,100,255));
      else
        rect.setFillColor(sf::Color::Blue);
      rect.setOutlineColor(makeDarkness(rect.getFillColor()));
      app->draw(rect);
    }
  }
  if(nend){
    Node* temp = nend;
    while(temp->parent){
      sf::Vertex new_line[2];
      new_line[0] = sf::Vertex(sf::Vector2f(temp->x * sparcing + sparcing/2, temp->y * sparcing  + sparcing/2));
      new_line[1] = sf::Vertex(sf::Vector2f(temp->parent->x * sparcing  + sparcing/2, temp->parent->y * sparcing  + sparcing/2));
      app->draw(new_line, 2, sf::Lines);
      temp = temp->parent;
    }
  }
}

void PathFinder::buildRegularGraph(){
  nodes.resize(size_h);
  uint32_t idy = 0;
  for(std::vector<Node>& line : nodes){
    for(uint32_t idx = 0; idx < size_w; ++idx){
      Node new_node;
      new_node.x = idx;
      new_node.y = idy;
      line.push_back(new_node);
    }
    ++idy;
  }
  for(std::vector<Node>& line : nodes){
    for(Node& node : line){
      if(node.x < size_w - 1){
        node.neighbours.push_back(&nodes[node.y][node.x + 1]);
        if(node.y < size_h - 1)
          node.neighbours.push_back(&nodes[node.y + 1][node.x + 1]);
        if(node.y > 0)
          node.neighbours.push_back(&nodes[node.y - 1][node.x + 1]);
      }
      if(node.x > 0){
        node.neighbours.push_back(&nodes[node.y][node.x - 1]);
        if(node.y < size_h - 1)
          node.neighbours.push_back(&nodes[node.y + 1][node.x - 1]);
        if(node.y > 0)
          node.neighbours.push_back(&nodes[node.y - 1][node.x - 1]);
      }
      if(node.y < size_h - 1)
        node.neighbours.push_back(&nodes[node.y + 1][node.x]);
      if(node.y > 0)
        node.neighbours.push_back(&nodes[node.y - 1][node.x]);
    }
  }
}

void PathFinder::update(){
  buildRegularGraph();
  sf::Event action;
  sf::Vector2i mouse_pos;
  camera.setCenter(sf::Vector2f(size_w*sparcing/2,size_h*sparcing/2));
  while(app->isOpen()){
    app->clear();
    app->setView(camera);
    mouse_pos = sf::Mouse::getPosition(*app);
    while(app->pollEvent(action)){
      if(action.type == sf::Event::Closed)
        app->close();
      if(action.type == sf::Event::KeyPressed){
        if(KEYBOARD(KEY_BEGIN_CELL)){
          clearVisited();
          set_mode_status = SET_MODE_BEGIN_CELL;
          std::cout << "Status: SETTING BEGIN_CELL\n";
        }
        if(KEYBOARD(KEY_END_CELL)){
          clearVisited();
          set_mode_status = SET_MODE_END_CELL;
          std::cout << "Status: SETTING END_CELL\n";
        }
        if(KEYBOARD(KEY_PUT_OBSTACLE)){
          clearVisited();
          set_mode_status = SET_MODE_OBSTACLE;
          std::cout << "Status: SETTING OBSTACLES\n";
        }
        if(KEYBOARD(KEY_REM_OBSTACLE)){
          clearVisited();
          set_mode_status = SET_MODE_NORMAL;
          std::cout << "Status: REMOVING OBSTACLES\n";
        }
        if(KEYBOARD(KEY_RESET_GRAPH)){
          resetGraph();
          std::cout << "Status: RESET GRAPH\n";
        }
        if(KEYBOARD(KEY_CLEAR_VISITED)){
          clearVisited();
          std::cout << "Status: CLEAR VISITED\n";
        }
        if(KEYBOARD(KEY_RUN_ALGORITHM)){
          if(nbegin && nend){
            clearVisited();
            if(id_algorithm == ID_A_STAR){
              aStar(*nbegin,*nend);
            }
            else if(id_algorithm ==ID_BFS){
              bfs(*nbegin);
            }
            else if(id_algorithm == ID_DFS){
              dfs(*nbegin);
            }

          }
        }
        if(KEYBOARD(KEY_NEXT_ALGORITHM)){
          id_algorithm = (1 + id_algorithm) % ALG_LIMIT;
          printCurrentAlgorithm();
        }
        if(KEYBOARD(KEY_PREV_ALGORITHM)){
          id_algorithm = (ALG_LIMIT - 1 + id_algorithm) % ALG_LIMIT;
          printCurrentAlgorithm();
        }
      }
      if (sf::Mouse::isButtonPressed(sf::Mouse::Left)){
        sf::Vector2f relative = app->mapPixelToCoords(mouse_pos);
        //std::cout << (int)relative.x/sparcing << ' ' << (int)relative.y/sparcing << std::endl;
        if(!((relative.x < 0 || relative.x > nodes[0].size()*sparcing) || (relative.y < 0 || relative.y > nodes.size()*sparcing))){
          if(set_mode_status == SET_MODE_BEGIN_CELL){
            if(nbegin) nbegin->isBegin = false;
            nbegin = &nodes[relative.y / sparcing][relative.x / sparcing];
            nbegin->isBegin = true;
            nbegin->isObstacle = false;
          }
          if(set_mode_status == SET_MODE_END_CELL){
            if(nend) nend->isEnd = false;
            nend = &nodes[relative.y / sparcing][relative.x / sparcing];
            nend->isEnd = true;
            nend->isObstacle = false;
          }
          if(set_mode_status == SET_MODE_OBSTACLE || set_mode_status == SET_MODE_NORMAL){
            Node* temp = &nodes[relative.y / sparcing][relative.x / sparcing];
            temp->isObstacle = (set_mode_status == SET_MODE_OBSTACLE)?1:0;
            temp->parent = nullptr;
            if(temp->isBegin) {temp->isBegin = false; nbegin = nullptr;}
            else if(temp->isEnd) {temp->isEnd = false; nend = nullptr;}
          }
        }
      }
    }
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
    showGraph();
    app->display();
  }
}
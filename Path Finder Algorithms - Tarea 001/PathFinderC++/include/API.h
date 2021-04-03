#ifndef API_H_
#define API_H_

#include <array>
#include <iostream>
#include <SFML/Graphics.hpp>

#include "A_Star.h"
#include "BFS.h"
#include "DFS.h"
#include "Settings.h"

sf::Color makeDarkness(const sf::Color& color);

class PathFinder{
  uint32_t size_w, size_h;
  uint32_t sparcing;

  std::vector<std::vector<Node>> nodes;
  Node* nbegin, *nend;

  std::unique_ptr<sf::RenderWindow> app;
  sf::View camera;
  uint32_t set_mode_status;

  uint32_t id_algorithm;

  sf::Font arial_font;
  sf::Text info;

  float delta_time;
public:
  PathFinder();
  void onSettingsText();
  void setStringInfo();
  void printCurrentAlgorithm();
  void clearVisited();
  void buildRegularGraph();
  void resetGraph();
  void showGraph();
  void update();
};

#endif//API_H_
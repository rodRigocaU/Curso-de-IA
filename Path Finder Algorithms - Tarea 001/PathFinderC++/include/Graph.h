#ifndef GRAPH_H_
#define GRAPH_H_

#include <vector>
#include <memory>

#include "Settings.h"

struct Node{
  bool isObstacle = false;
  bool isVisited = false;
  bool isBegin = false;
  bool isEnd = false;
  float global_distance_to_end = INFINITY_FLOAT;
  float local_distance_from_begin = INFINITY_FLOAT;
  uint32_t x = 0, y = 0;
  Node* parent = nullptr;
  std::vector<Node*> neighbours;
};

#endif//GRAPH_H_
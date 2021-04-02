#ifndef GRAPH_H_
#define GRAPH_H_

#include <vector>
#include <memory>

struct Node{
  bool isObstacle = false;
  bool isVisited = false;
  bool isBegin = false;
  bool isEnd = false;
  uint32_t x = 0, y = 0;
  Node* parent = nullptr;
  std::vector<Node*> neighbours;
};

#endif//GRAPH_H_
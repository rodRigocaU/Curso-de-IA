#include "../include/HillClimbing.h"

float heuristicDistance(Node &ori, Node &dest) {
  return std::max(std::abs(int(ori.x - dest.x)), std::abs(int(ori.y - dest.y)));
}

void hillClimbing(Node &begin, Node &end){
  std::queue<Node*> listNodesToTest;
  Node* currentNode = &begin;
  listNodesToTest.push(currentNode);
  while(!listNodesToTest.empty() && !currentNode->isEnd){
    currentNode = listNodesToTest.front();
    listNodesToTest.pop();
    std::list<Node*> sorted_successors;
    for(Node* successor : currentNode->neighbours){
      if(!successor->isVisited && !successor->isObstacle){
        successor->global_distance_to_end = heuristicDistance(*successor, end);
        successor->parent = currentNode;
        successor->isVisited = true;
        sorted_successors.push_back(successor);
      }
    }
    sorted_successors.sort([](const Node* lhs, const Node* rhs){return lhs->global_distance_to_end > rhs->global_distance_to_end;});
    while(!sorted_successors.empty()){
      listNodesToTest.push(sorted_successors.front());
      sorted_successors.pop_front();
    }
  }
}

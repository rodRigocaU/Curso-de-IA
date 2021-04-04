#include "../include/A_Star.h"

float euclideanDistance(Node &ori, Node &dest)
{
  return sqrt(pow((int(ori.x - dest.x)), 2) + pow(int(ori.y - dest.y), 2));
}

float diagonalDistance(Node &ori, Node &dest)
{
  return std::max(std::abs(int(ori.x - dest.x)), std::abs(int(ori.y - dest.y)));
}

float manhattanDistance(Node &ori, Node &dest)
{
  return std::abs(int(ori.x - dest.x)) + std::abs(int(ori.y - dest.y));
}

bool compareNodes(const Node* lhs, Node* rhs){
  return (lhs->global_distance_to_end < rhs->global_distance_to_end);
}

void aStar(Node &begin, Node &end, std::function<float(Node&,Node&)> heuristic){
  Node* currentNode = &begin;
  currentNode->local_distance_from_begin = 0.0;
  currentNode->global_distance_to_end = heuristic(begin, end);

  std::vector<Node*> listNodesToTest;
  listNodesToTest.push_back(currentNode);

  while(!listNodesToTest.empty() && !currentNode->isEnd){
    std::sort(listNodesToTest.begin(), listNodesToTest.end(), compareNodes);

    while(!listNodesToTest.empty() && listNodesToTest[0]->isVisited)
      listNodesToTest.erase(listNodesToTest.begin());

    if(!listNodesToTest.empty()){
      currentNode = listNodesToTest[0];
      currentNode->isVisited = true;

      for(Node* neighbor : currentNode->neighbours){
        if(!neighbor->isVisited && !neighbor->isObstacle){
          listNodesToTest.push_back(neighbor);

          float possibleLowerDistance = currentNode->local_distance_from_begin + diagonalDistance(*currentNode, *neighbor);
            
          if(possibleLowerDistance < neighbor->local_distance_from_begin){
            neighbor->parent = currentNode;
            neighbor->local_distance_from_begin = possibleLowerDistance;
            neighbor->global_distance_to_end = neighbor->local_distance_from_begin + heuristic(*neighbor, end);
          }
        }
      }
    }
  }
}
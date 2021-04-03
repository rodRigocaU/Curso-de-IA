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
/*
bool compare(const std::pair<float, Node *> &a, const std::pair<float, Node *> &b)
{
  return (a.first < b.first);
}

void aStar(Node &begin, Node &end)
{
  // std::vector<std::pair<float, Node *>> disVe; //Euclidiana
  std::vector<std::pair<int, Node *>> disVe;

  Node *n = &begin;
  // std::vector<Node*>

  while (!n->isEnd)
  {
    for (Node *it : n->neighbours)
      if (!it->isObstacle && !it->isVisited)
      //if (!it->isObstacle)
        disVe.push_back(std::make_pair(diagonalDistance(*it, end), it));
        // disVe.push_back(std::make_pair(euclideanDistance(*it, end), it));
        // disVe.push_back(std::make_pair(manhattanDistance(*it, end), it));

    //SORT
    // std::sort(disVe.begin(), disVe.end());
    std::sort(disVe.begin(), disVe.end(), compare);

    if (disVe.size())
    {
      disVe[0].second->parent = n;
      n = disVe[0].second;
      n->isVisited = true;
      disVe.clear();
    }
    else
      break;
    
  }
}*/

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
#include "../include/A_Star.h"

float diseucli(Node &ori, Node &dest)
{
  return sqrt(pow((int(ori.x - dest.x)), 2) + pow(int(ori.y - dest.y), 2));
}

int disdiago(Node &ori, Node &dest)
{
  return std::max(std::abs(int(ori.x - dest.x)), std::abs(int(ori.y - dest.y)));
}

int disman(Node &ori, Node &dest)
{
  return std::abs(int(ori.x - dest.x)) + std::abs(int(ori.y - dest.y));
}

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
        disVe.push_back(std::make_pair(disdiago(*it, end), it));
        // disVe.push_back(std::make_pair(diseucli(*it, end), it));
        // disVe.push_back(std::make_pair(disman(*it, end), it));

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
}
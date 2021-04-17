#ifndef A_STAR_H_
#define A_STAR_H_

#include <algorithm>
#include <functional>
#include <iostream>
#include <math.h>
#include <vector>
#include <utility>

#include "Graph.h"

float euclideanDistance(Node& ori,Node& dest);
float diagonalDistance(Node &ori, Node &dest);
float manhattanDistance(Node &ori, Node &dest);
//bool compare(const std::pair<float, Node *> &a, const std::pair<float, Node *> &b);
//void aStar(Node& begin, Node& end);
void aStar(Node &begin, Node &end, std::function<float(Node&,Node&)> heuristic = diagonalDistance);

#endif
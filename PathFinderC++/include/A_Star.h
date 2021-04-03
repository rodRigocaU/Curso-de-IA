#ifndef A_STAR_H_
#define A_STAR_H_

#include "Graph.h"
#include <algorithm>
#include <math.h>
#include <vector>
#include <utility>

float diseucli(Node& ori,Node& dest);
int disdiago(Node &ori, Node &dest);
int disman(Node &ori, Node &dest);
bool compare(const std::pair<float, Node *> &a, const std::pair<float, Node *> &b);
void aStar(Node& begin, Node& end);

#endif
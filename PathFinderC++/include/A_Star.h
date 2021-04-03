#ifndef A_STAR_H_
#define A_STAR_H_

#include "Graph.h"
#include <algorithm>
#include <math.h>
#include <vector>
#include <utility>

float diseucli(Node& ori,Node& dest);
void aStar(Node& begin, Node& end);

#endif
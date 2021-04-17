#include "../include/BFS.h"

void bfs(Node& begin){
  std::queue<Node*> q_bfs;
  begin.isVisited = true;
  q_bfs.push(&begin);
  while(!q_bfs.empty()){
    for(Node* neighbor : q_bfs.front()->neighbours){
      if(!neighbor->isVisited && !neighbor->isObstacle){
        neighbor->parent = q_bfs.front();
        neighbor->isVisited = true;
        if(neighbor->isEnd)
          return;
        q_bfs.push(neighbor);
      }
    }
    q_bfs.pop();
  }
}

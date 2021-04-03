#include "../include/DFS.h"

void dfs(Node& begin){
  std::stack<Node*> s_dfs;
  begin.isVisited = true;
  s_dfs.push(&begin);
  while(!s_dfs.empty()){
    Node* temp = s_dfs.top();
    s_dfs.pop();
    for(Node* neighbor : temp->neighbours){
      if(!neighbor->isVisited && !neighbor->isObstacle){
        neighbor->parent = temp;
        neighbor->isVisited = true;
        if(neighbor->isEnd)
          return;
        s_dfs.push(neighbor);
      }
    }
  }
}
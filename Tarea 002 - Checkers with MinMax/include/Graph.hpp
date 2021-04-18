#ifndef GRAPH_HPP_
#define GRAPH_HPP_

#include <functional>
#include <iostream>
#include <limits>
#include <list>
#include <string>


namespace graph{

enum LevelType{MIN, MAX};

class Node{
private:
  int8_t value_;
  std::string movement_;
  std::list<std::shared_ptr<Node>> successors;
  bool wasPruned;
public:
  Node();
  void setMovement(const std::string& movement);
  void setValue(const int8_t& value);
  void setSuccessor(const int8_t& value, const std::string& movement);
  void pruneBranch();
  Node* searchSuccessor(LevelType levelType);
  bool isLeaf();
  std::list<std::shared_ptr<Node>>& getSuccessorsList();
};

//#################################################################
//#################################################################
//#################################################################

Node::Node(){
  value_ = 0;
  wasPruned = false;
}

void Node::setMovement(const std::string& movement){
  movement_ = movement;
}

Node* Node::searchSuccessor(LevelType levelType){
  Node* selectedNode = nullptr;
  int8_t minmaxValue = 0;
  std::function<bool(const int8_t&,const int8_t&)> comparator;
  switch(levelType){
    case LevelType::MAX:
      comparator = [](const int8_t& A,const int8_t& B){return A > B;};
      minmaxValue = std::numeric_limits<int8_t>::min();
      break;
    case LevelType::MIN:
      comparator = [](const int8_t& A,const int8_t& B){return A < B;};
      minmaxValue = std::numeric_limits<int8_t>::max();
      break;
  }
  for(std::shared_ptr<Node>& successor : successors)
    if(comparator(successor->value_, minmaxValue) && !successor->wasPruned)
      selectedNode = successor.get();
  return selectedNode;
}

void Node::setValue(const int8_t& value){
  value_ = value;
}

void Node::setSuccessor(const int8_t& value, const std::string& movement){
  successors.push_back(std::make_shared<Node>());
  successors.back()->setValue(value);
  successors.back()->setMovement(movement);
}

void Node::pruneBranch(){
  wasPruned = true;
}

bool Node::isLeaf(){
  return successors.empty();
}

std::list<std::shared_ptr<Node>>& Node::getSuccessorsList(){
  return successors;
}


}

#endif//GRAPH_HPP_
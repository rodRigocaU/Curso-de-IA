#ifndef API_HPP_
#define API_HPP_

#include <iostream>

#include <SFML/Graphics.hpp>

#include "Token.hpp"

namespace AI{

enum Movement{ILLEGAL, SIMPLE, MURDERER};

class CheckersGame{
private:
  const uint32_t SIZE_HUD = 155;
  //Checker's board (-1 -> bot) && (1 -> human)
  short mboard[8][8] = {-1, 0,-1, 0,-1, 0,-1, 0,
                        0,-1, 0,-1, 0,-1, 0,-1,
                        -1, 0,-1, 0,-1, 0,-1, 0,
                        0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0,
                        0, 1, 0, 1, 0, 1, 0, 1,
                        1, 0, 1, 0, 1, 0, 1, 0,
                        0, 1, 0, 1, 0, 1, 0, 1 };
  Turn gameState;
  std::vector<Token> humanTokens, botTokens;
  Token* currentHumanTokenSelected;
  sf::Texture tokenTexture, board;
  float offSet;

  void setInitialPositions();
  Movement validateMovement(Turn currentTurn, const sf::Vector2<int8_t>& begin, const sf::Vector2<int8_t>& end);
  void onControlsUpdate(sf::RenderWindow& window);
  void displayGame(sf::RenderWindow& window);
public:
  void start();
};

//#################################################################
//#################################################################
//#################################################################

void CheckersGame::setInitialPositions(){
  offSet = 0;
  for(std::size_t y = 0; y < 8; ++y)
    for(std::size_t x = 0; x < 8; ++x){
      if(mboard[y][x] == 1){
        humanTokens.emplace_back(Turn::HUMAN, tokenTexture, x, y);
        humanTokens.back().setOffSet(offSet);
      }
      else if(mboard[y][x] == -1){
        botTokens.emplace_back(Turn::BOT, tokenTexture, x, y);
        botTokens.back().setOffSet(offSet);
      }
    }
}

void CheckersGame::displayGame(sf::RenderWindow& window){
  for(Token& token : humanTokens)
    token.display(window);
  for(Token& token : botTokens)
    token.display(window);
}

Movement CheckersGame::validateMovement(Turn currentTurn, const sf::Vector2<int8_t>& begin, const sf::Vector2<int8_t>& end){
  if(end.x >= 0 && end.y >= 0 && end.x < 8 && end.y < 8){
    switch(currentTurn){
      case Turn::HUMAN:
        if(begin.y > end.y) {
          if(mboard[end.y][end.x] == 0){//if end is not occupated by another human's token
            return Movement::SIMPLE;
          }
          else if(mboard[end.y][end.x] == -1){//if end is occupated by a bot's token
            if((end.x - begin.x) < 8 && (end.y - begin.y) < 8 && mboard[2*end.y - begin.y][2*end.x - begin.x] == 0)
              return Movement::MURDERER;
          }
        }
        break;
      case Turn::BOT:
        if(begin.y < end.y) {
          if(mboard[end.y][end.x] == 0){//if end is not occupated by another bot's token
            return Movement::SIMPLE;
          }
          else if(mboard[end.y][end.x] == 1){//if end is occupated by a human's token
            if((end.x - begin.x) < 8 && (end.y - begin.y) < 8 && mboard[2*end.y - begin.y][2*end.x - begin.x] == 0)
              return Movement::MURDERER;
          }
        }
        break;
    }
  }
  return Movement::ILLEGAL;
}

void CheckersGame::onControlsUpdate(sf::RenderWindow& window){
  switch(gameState){
    case Turn::HUMAN:
      if(sf::Mouse::isButtonPressed(sf::Mouse::Button::Left) && humanTokens.size() > 0){
        currentHumanTokenSelected = nullptr;
        sf::Vector2i mousePosition = sf::Mouse::getPosition(window);
        for(Token& token : humanTokens){
          if(token.checkOverlap(mousePosition)){
            currentHumanTokenSelected = &token;
            break;
          }
        }
      }
      if(currentHumanTokenSelected){
        if(sf::Keyboard::isKeyPressed(sf::Keyboard::Left)){
          Movement moveType = validateMovement(Turn::HUMAN, currentHumanTokenSelected->getGlobalPosition(), currentHumanTokenSelected->getGlobalPosition() + sf::Vector2<int8_t>(-1,-1));
          gameState = Turn::BOT;
          if(moveType == Movement::SIMPLE)
            currentHumanTokenSelected->changePosition(currentHumanTokenSelected->getGlobalPosition() + sf::Vector2<int8_t>(-1,-1));
          else if(moveType == Movement::MURDERER)
            currentHumanTokenSelected->changePosition(currentHumanTokenSelected->getGlobalPosition() + sf::Vector2<int8_t>(-2,-2));
          else if(moveType == Movement::ILLEGAL)
            gameState = Turn::HUMAN;
        }
        else if(sf::Keyboard::isKeyPressed(sf::Keyboard::Right)){
          Movement moveType = validateMovement(Turn::HUMAN, currentHumanTokenSelected->getGlobalPosition(), currentHumanTokenSelected->getGlobalPosition() + sf::Vector2<int8_t>(1,-1));
          gameState = Turn::BOT;
          if(moveType == Movement::SIMPLE)
            currentHumanTokenSelected->changePosition(currentHumanTokenSelected->getGlobalPosition() + sf::Vector2<int8_t>(1,-1));
          else if(moveType == Movement::MURDERER)
            currentHumanTokenSelected->changePosition(currentHumanTokenSelected->getGlobalPosition() + sf::Vector2<int8_t>(2,-2));
          else if(moveType == Movement::ILLEGAL)
            gameState = Turn::HUMAN;
        }
      }
      break;
    case Turn::BOT:
      //min max
      break;
  }
}

void CheckersGame::start(){
  gameState = Turn::HUMAN;
  sf::RenderWindow app(sf::VideoMode(617,617 + SIZE_HUD), "Checkers Game");
  app.setFramerateLimit(60);

  sf::Event action;

  board.loadFromFile("assets/Board.jpg");
  tokenTexture.loadFromFile("assets/CheckersToken.png");
  sf::Sprite displayableBoard; displayableBoard.setTexture(board);
  displayableBoard.setScale(app.getSize().x / displayableBoard.getGlobalBounds().getSize().x,
                            (app.getSize().y - SIZE_HUD) / displayableBoard.getGlobalBounds().getSize().y);
  
  setInitialPositions();
  while(app.isOpen()){
    while(app.pollEvent(action)){
      if(action.type == sf::Event::Closed){
        app.close();
      }
    }
    onControlsUpdate(app);
    app.clear();
    app.draw(displayableBoard);
    displayGame(app);
    app.display();
  }
}

}

#endif//API_HPP_

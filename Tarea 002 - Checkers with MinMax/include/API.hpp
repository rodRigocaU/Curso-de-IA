#ifndef API_HPP_
#define API_HPP_

#include <iostream>
#include <limits>

#include <SFML/Graphics.hpp>

namespace AI{

enum Movement{ILLEGAL, SIMPLE, MURDER};

enum Turn{BOT, HUMAN};

class CheckersGame{
private:
  const uint32_t SIZE_HUD = 155;
  struct GameStatus{
    int8_t botTokenCount, humanTokenCount;
    short mSimulationBoard[8][8] = {0};
    std::vector<GameStatus*> successors;
    bool gameOver();
  };

  //Checker's board (-1 -> bot) && (1 -> human)
  short backup[8][8] = {-1, 0,-1, 0,-1, 0,-1, 0,
                        0,-1, 0,-1, 0,-1, 0,-1,
                        -1, 0,-1, 0,-1, 0,-1, 0,
                        0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0,
                        0, 1, 0, 1, 0, 1, 0, 1,
                        1, 0, 1, 0, 1, 0, 1, 0,
                        0, 1, 0, 1, 0, 1, 0, 1 };
  short mboard[8][8] = {0};
  int8_t humanTokenCount, botTokenCount;
  Turn gameState;
  sf::Vector2<int8_t> currentHumanTokenSelected;
  sf::Texture tokenTexture, board;
  sf::Sprite tokenSprite;

  void setInitialPositions();
  void confirmMovement(short currentBoard[8][8], Movement moveType, const sf::Vector2<int8_t>& begin, const sf::Vector2<int8_t>& end);
  Movement validateMovement(Turn currentTurn, const sf::Vector2<int8_t>& begin, const sf::Vector2<int8_t>& end);
  void onControlsUpdate(sf::RenderWindow& window);
  int8_t minmaxAlphaBeta(GameStatus* currentGameState, uint32_t depth, Turn currentTurn, 
                      int8_t alpha = std::numeric_limits<int8_t>::min(), int8_t beta  = std::numeric_limits<int8_t>::max());
  void startSimulation(GameStatus* currentGameState);
  void displayGame(sf::RenderWindow& window);
public:
  void start();
};

//#################################################################
//#################################################################
//#################################################################

void CheckersGame::setInitialPositions(){
  tokenSprite.setTexture(tokenTexture);
  tokenSprite.setScale(0.15,0.15);
  humanTokenCount = botTokenCount = 12;
  for(std::size_t y = 0; y < 8; ++y)
    for(std::size_t x = 0; x < 8; ++x){
      mboard[y][x] = backup[y][x];
    }
}

void CheckersGame::displayGame(sf::RenderWindow& window){
  for(std::size_t y = 0; y < 8; ++y)
    for(std::size_t x = 0; x < 8; ++x){
      if(mboard[y][x] != 0){
        if(mboard[y][x] == 1)
          tokenSprite.setColor(sf::Color::Red);
        else if(mboard[y][x] == -1)
          tokenSprite.setColor(sf::Color(55,55,55));
        tokenSprite.setPosition(x * tokenSprite.getGlobalBounds().width, y * tokenSprite.getGlobalBounds().height);
        window.draw(tokenSprite);
        if(mboard[y][x] == 1 && sf::Vector2<int8_t>(x,y) == currentHumanTokenSelected){
          sf::RectangleShape target(sf::Vector2f(tokenSprite.getGlobalBounds().width, tokenSprite.getGlobalBounds().height));
          target.setPosition(sf::Vector2f(x * tokenSprite.getGlobalBounds().width, y * tokenSprite.getGlobalBounds().height));
          target.setOutlineColor(sf::Color::Green);
          target.setOutlineThickness(-4.5);
          target.setFillColor(sf::Color::Transparent);
          window.draw(target);
        }
      }
    }
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
            if((end.x - begin.x) >= 0 && (end.y - begin.y) >= 0 && (end.x - begin.x) < 8 && (end.y - begin.y) < 8 && mboard[2*end.y - begin.y][2*end.x - begin.x] == 0)
              return Movement::MURDER;
          }
        }
        break;
      case Turn::BOT:
        if(begin.y < end.y) {
          if(mboard[end.y][end.x] == 0){//if end is not occupated by another bot's token
            return Movement::SIMPLE;
          }
          else if(mboard[end.y][end.x] == 1){//if end is occupated by a human's token
            if((end.x - begin.x) >= 0 && (end.y - begin.y) >= 0 && (end.x - begin.x) < 8 && (end.y - begin.y) < 8 && mboard[2*end.y - begin.y][2*end.x - begin.x] == 0)
              return Movement::MURDER;
          }
        }
        break;
    }
  }
  return Movement::ILLEGAL;
}

void CheckersGame::confirmMovement(short currentBoard[8][8], Movement moveType, const sf::Vector2<int8_t>& begin, const sf::Vector2<int8_t>& end){
  sf::Vector2<int8_t> distance = end - begin;
  short token = (distance.y > 0)?-1:1;
  int8_t* tokenCount = (token == -1)?&humanTokenCount:&botTokenCount;
  switch(moveType){
    case Movement::ILLEGAL:
      return;
    case Movement::SIMPLE:
      currentBoard[begin.y][begin.x] = 0;
      currentBoard[end.y][end.x] = token;
      break;
    case Movement::MURDER:
      currentBoard[begin.y][begin.x] = 0;
      currentBoard[begin.y + distance.y/2][begin.x + distance.x/2] = 0;
      currentBoard[end.y][end.x] = token;
      --(*tokenCount);
      break;
  }
}

void CheckersGame::onControlsUpdate(sf::RenderWindow& window){
  switch(gameState){
    case Turn::HUMAN:
      if(sf::Mouse::isButtonPressed(sf::Mouse::Button::Left) && humanTokenCount > 0){
        currentHumanTokenSelected = sf::Vector2<int8_t>(-1,-1);
        sf::Vector2i mousePosition = sf::Vector2i(sf::Mouse::getPosition(window).x / int(tokenSprite.getGlobalBounds().width), sf::Mouse::getPosition(window).y / int(tokenSprite.getGlobalBounds().height));
        if(mboard[mousePosition.y][mousePosition.x] == 1){
          currentHumanTokenSelected = sf::Vector2<int8_t>(int8_t(mousePosition.x), int8_t(mousePosition.y));
        }
      }
      if(currentHumanTokenSelected != sf::Vector2<int8_t>(-1,-1)){
        if(sf::Keyboard::isKeyPressed(sf::Keyboard::Left)){
          Movement moveType = validateMovement(Turn::HUMAN, currentHumanTokenSelected, currentHumanTokenSelected + sf::Vector2<int8_t>(-1,-1));
          gameState = Turn::BOT;
          confirmMovement(mboard, moveType, currentHumanTokenSelected, currentHumanTokenSelected + sf::Vector2<int8_t>(-1,-1));
          if(moveType == Movement::ILLEGAL)
            gameState = Turn::HUMAN;   
          else
            currentHumanTokenSelected = sf::Vector2<int8_t>(-1,-1);
        }
        else if(sf::Keyboard::isKeyPressed(sf::Keyboard::Right)){
          Movement moveType = validateMovement(Turn::HUMAN, currentHumanTokenSelected, currentHumanTokenSelected + sf::Vector2<int8_t>(1,-1));
          gameState = Turn::BOT;
          confirmMovement(mboard, moveType, currentHumanTokenSelected, currentHumanTokenSelected + sf::Vector2<int8_t>(1,-1));
          if(moveType == Movement::ILLEGAL)
            gameState = Turn::HUMAN;
          else
            currentHumanTokenSelected = sf::Vector2<int8_t>(-1,-1);
        }
      }
      break;
    case Turn::BOT:
      //min max
      gameState = Turn::HUMAN;
      break;
  }
}

int8_t CheckersGame::minmaxAlphaBeta(GameStatus* currentGameState, uint32_t depth, Turn currentTurn, int8_t alpha = std::numeric_limits<int8_t>::min(), int8_t beta  = std::numeric_limits<int8_t>::max()){
  if(depth == 0 || currentGameState->gameOver())
    return currentGameState->botTokenCount - currentGameState->humanTokenCount;
  switch(currentTurn){
    case Turn::BOT:
      break;
    case Turn::HUMAN:
      break;
  }
}

void CheckersGame::startSimulation(GameStatus* currentGameState){
  if(currentGameState){
    
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

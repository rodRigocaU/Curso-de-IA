#ifndef API_HPP_
#define API_HPP_

#include <algorithm>
#include <iostream>
#include <limits>
#include <memory>
#include <string>

#include <SFML/Graphics.hpp>

namespace AI{

std::size_t fileCounter = 1;

enum Movement{ILLEGAL, SIMPLE, MURDER};

enum Turn{BOT, HUMAN};

enum Direction{LEFT, RIGHT};

class CheckersGame{
private:
  const uint32_t SIZE_HUD = 155;
  struct GameStatus{
    int8_t botTokenCount, humanTokenCount;
    int8_t value;
    Direction currentDir2Check;
    std::size_t auxidx, auxidy;
    short mSimulationBoard[8][8] = {0};
    std::vector<std::shared_ptr<GameStatus>> successors;

    GameStatus(short currentBoard[8][8]){
      botTokenCount = humanTokenCount = 0;
      value = 0;
      auxidx = auxidy = 0;
      currentDir2Check = Direction::LEFT;
      setBoard(currentBoard);
    }

    void setBoard(short currentBoard[8][8]){
      for(std::size_t y = 0; y < 8; ++y)
        for(std::size_t x = 0; x < 8; ++x){
          mSimulationBoard[y][x] = currentBoard[y][x];
          if(mSimulationBoard[y][x] == 2) ++botTokenCount;
          else if(mSimulationBoard[y][x] == 1) ++humanTokenCount;
        }
    }
  };

  //Checker's board (2 -> bot) && (1 -> human)
  short backup[8][8] = {2, 0, 2, 0, 2, 0, 2, 0,
                        0, 2, 0, 2, 0, 2, 0, 2,
                        2, 0, 2, 0, 2, 0, 2, 0,
                        0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0,
                        0, 1, 0, 1, 0, 1, 0, 1,
                        1, 0, 1, 0, 1, 0, 1, 0,
                        0, 1, 0, 1, 0, 1, 0, 1 };
  short mboard[8][8] = {0};
  int8_t humanTokenCount, botTokenCount;
  Turn gameTurn, startTurn = Turn::HUMAN;
  bool gameFinished;

  uint32_t treeDepth;
  std::shared_ptr<GameStatus> root, choosenBotMovement;

  sf::Vector2<int8_t> currentHumanTokenSelected;
  sf::Texture tokenTexture, board;
  sf::Sprite tokenSprite;
  sf::Time botThinkDelay;
  sf::Clock botMovementTimer;
  sf::Font arialFont;
  sf::Text hudDisplayedInfo, winnerDisplayed;

  void setInitialPositions();
  void displayHUDInfo(sf::RenderWindow& window);
  void confirmMovement(short currentBoard[8][8], Movement moveType, const sf::Vector2<int8_t>& begin, const sf::Vector2<int8_t>& end);
  Movement validateMovement(short currentBoard[8][8], Turn currentTurn, const sf::Vector2<int8_t>& begin, const sf::Vector2<int8_t>& end);
  void onControlsUpdate(sf::RenderWindow& window);
  void onHUDControlsUpdate(sf::RenderWindow& window, const sf::Event& event);
  int8_t minmaxAlphaBeta(std::shared_ptr<GameStatus> currentGameState, uint32_t depth, Turn currentTurn, 
                      int8_t alpha = std::numeric_limits<int8_t>::min(), int8_t beta  = std::numeric_limits<int8_t>::max());
  bool getNextSimulation(Turn currentTurn, std::shared_ptr<GameStatus> currentGameState);
  void displayGame(sf::RenderWindow& window);
  bool gameOver(Turn currentTurn, std::shared_ptr<GameStatus> currentGameState);
public:
  void start();
};

//#################################################################
//#################################################################
//#################################################################

void CheckersGame::setInitialPositions(){
  gameTurn = startTurn;
  gameFinished = false;
  tokenSprite.setTexture(tokenTexture);
  tokenSprite.setScale(0.15,0.15);
  humanTokenCount = botTokenCount = 12;
  for(std::size_t y = 0; y < 8; ++y)
    for(std::size_t x = 0; x < 8; ++x){
      mboard[y][x] = backup[y][x];
    }
  botMovementTimer.restart();
}
//#tokens H B, turn, depth, depth in words, initial turn 
void CheckersGame::displayHUDInfo(sf::RenderWindow& window){
  std::string rawHUDInfo = "A.I. process delay: " + ((botThinkDelay.asSeconds() > 0)?std::to_string(botThinkDelay.asSeconds()) + " seconds":"NoWait") + ".\n";
  rawHUDInfo += "A.I. depth: <" + std::to_string(treeDepth) + ">\t";
  rawHUDInfo += "Game Level: [";
  switch(treeDepth){
    case 1:
      rawHUDInfo += "Noob/Easy";
      break;
    case 2:
      rawHUDInfo += "Enthusiast/Medium";
      break;
    case 3:
      rawHUDInfo += "Advanced/Hard";
      break;
    case 4:
      rawHUDInfo += "Competitive";
      break;
    case 5:
      rawHUDInfo += "Master";
      break;
    case 6:
      rawHUDInfo += "Grand Master";
      break;
    case 7:
      rawHUDInfo += "Legendary";
      break;
  }
  rawHUDInfo += "]\n";
  rawHUDInfo += "Current turn: <" + std::string((gameTurn == Turn::HUMAN)?"Human":"A.I.") + ">\n";
  rawHUDInfo += "Starter in the next game: [" + std::string((startTurn == Turn::HUMAN)?"Human":"A.I.") + "]\n";
  rawHUDInfo += "#Human Tokens: " + std::to_string(int(humanTokenCount)) + " vs #A.I. Tokens: " + std::to_string(int(botTokenCount)) + "\n";
  hudDisplayedInfo.setString(rawHUDInfo);
  window.draw(hudDisplayedInfo);
}

void CheckersGame::displayGame(sf::RenderWindow& window){
  for(std::size_t y = 0; y < 8; ++y)
    for(std::size_t x = 0; x < 8; ++x){
      if(mboard[y][x] != 0){
        if(mboard[y][x] == 1)
          tokenSprite.setColor(sf::Color::Red);
        else if(mboard[y][x] == 2)
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

void CheckersGame::onHUDControlsUpdate(sf::RenderWindow& window, const sf::Event& event){
  if(event.type == sf::Event::KeyPressed){
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Add)){
      ++treeDepth;
      if(treeDepth > 7)
        treeDepth = 7;
    }
    else if(sf::Keyboard::isKeyPressed(sf::Keyboard::Subtract)){
      --treeDepth;
      if(treeDepth > 7 || treeDepth == 0)
        treeDepth = 1;
    }
    else if(sf::Keyboard::isKeyPressed(sf::Keyboard::C)){
      startTurn = (startTurn == Turn::HUMAN)?Turn::BOT:Turn::HUMAN;
    }
    else if(sf::Keyboard::isKeyPressed(sf::Keyboard::F)){
      gameFinished = true;
    }
    else if(sf::Keyboard::isKeyPressed(sf::Keyboard::R)){
      setInitialPositions();
    }
    else if(sf::Keyboard::isKeyPressed(sf::Keyboard::S)){
      sf::Vector2u windowSize = window.getSize();
      sf::Texture captureTexture;
      captureTexture.create(windowSize.x, windowSize.y);
      captureTexture.update(window);
      sf::Image screenshot = captureTexture.copyToImage();
      screenshot.saveToFile("../screenshots/" + std::to_string(fileCounter++) + ".jpg");
    }
  }
}

Movement CheckersGame::validateMovement(short currentBoard[8][8], Turn currentTurn, const sf::Vector2<int8_t>& begin, const sf::Vector2<int8_t>& end){
  if(end.x >= 0 && end.y >= 0 && end.x < 8 && end.y < 8){
    switch(currentTurn){
      case Turn::HUMAN:
        if(begin.y > end.y) {
          if(currentBoard[end.y][end.x] == 0){//if end is not occupated by another human's token
            return Movement::SIMPLE;
          }
          else if(currentBoard[end.y][end.x] == 2){//if end is occupated by a bot's token
            if((2*end.x - begin.x) >= 0 && (2*end.y - begin.y) >= 0 && (2*end.x - begin.x) < 8 && (2*end.y - begin.y) < 8)
              if(currentBoard[2*end.y - begin.y][2*end.x - begin.x] == 0)
                return Movement::MURDER;
          }
        }
        break;
      case Turn::BOT:
        if(begin.y < end.y) {
          if(currentBoard[end.y][end.x] == 0){//if end is not occupated by another bot's token
            return Movement::SIMPLE;
          }
          else if(currentBoard[end.y][end.x] == 1){//if end is occupated by a human's token
            if((2*end.x - begin.x) >= 0 && (2*end.y - begin.y) >= 0 && (2*end.x - begin.x) < 8 && (2*end.y - begin.y) < 8)
              if(currentBoard[2*end.y - begin.y][2*end.x - begin.x] == 0)
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
  short token = (distance.y > 0)?2:1;
  switch(moveType){
    case Movement::ILLEGAL:
      return;
    case Movement::SIMPLE:
      currentBoard[begin.y][begin.x] = 0;
      currentBoard[end.y][end.x] = token;
      break;
    case Movement::MURDER:
      currentBoard[begin.y][begin.x] = 0;
      currentBoard[end.y][end.x] = 0;
      currentBoard[end.y + distance.y][end.x + distance.x] = token;
      break;
  }
}

void CheckersGame::onControlsUpdate(sf::RenderWindow& window){
  switch(gameTurn){
    case Turn::HUMAN:
      if(sf::Mouse::isButtonPressed(sf::Mouse::Button::Left) && humanTokenCount > 0){
        currentHumanTokenSelected = sf::Vector2<int8_t>(-1,-1);
        sf::Vector2i mousePosition = sf::Vector2i(sf::Mouse::getPosition(window).x / int(tokenSprite.getGlobalBounds().width), sf::Mouse::getPosition(window).y / int(tokenSprite.getGlobalBounds().height));
        if(mboard[mousePosition.y][mousePosition.x] == 1){
          currentHumanTokenSelected = sf::Vector2<int8_t>(int8_t(mousePosition.x), int8_t(mousePosition.y));
        }
      }
      if(currentHumanTokenSelected != sf::Vector2<int8_t>(-1,-1)){
        if(sf::Keyboard::isKeyPressed(sf::Keyboard::A)){
          Movement moveType = validateMovement(mboard, Turn::HUMAN, currentHumanTokenSelected, currentHumanTokenSelected + sf::Vector2<int8_t>(-1,-1));
          confirmMovement(mboard, moveType, currentHumanTokenSelected, currentHumanTokenSelected + sf::Vector2<int8_t>(-1,-1));
          if(moveType != Movement::ILLEGAL){
            if(moveType == Movement::MURDER)
              --botTokenCount;
            gameTurn = Turn::BOT;   
            currentHumanTokenSelected = sf::Vector2<int8_t>(-1,-1);
            gameFinished = gameOver(gameTurn, std::make_shared<GameStatus>(mboard));
          }
        }
        else if(sf::Keyboard::isKeyPressed(sf::Keyboard::D)){
          Movement moveType = validateMovement(mboard, Turn::HUMAN, currentHumanTokenSelected, currentHumanTokenSelected + sf::Vector2<int8_t>(1,-1));
          confirmMovement(mboard, moveType, currentHumanTokenSelected, currentHumanTokenSelected + sf::Vector2<int8_t>(1,-1));
          if(moveType != Movement::ILLEGAL){
            if(moveType == Movement::MURDER)
              --botTokenCount;
            gameTurn = Turn::BOT;   
            currentHumanTokenSelected = sf::Vector2<int8_t>(-1,-1);
            gameFinished = gameOver(gameTurn, std::make_shared<GameStatus>(mboard));
          }
        }
      }
      botMovementTimer.restart();
      break;
    case Turn::BOT:
      if(botMovementTimer.getElapsedTime() >= botThinkDelay){
        root = std::make_shared<GameStatus>(mboard);
        minmaxAlphaBeta(root, treeDepth, gameTurn);
        if(choosenBotMovement != nullptr){
          humanTokenCount = choosenBotMovement->humanTokenCount;
          botTokenCount = choosenBotMovement->botTokenCount;
          for(std::size_t y = 0; y < 8; ++y)
            for(std::size_t x = 0; x < 8; ++x){
              mboard[y][x] = choosenBotMovement->mSimulationBoard[y][x];
            }
        }
        gameTurn = Turn::HUMAN;
        gameFinished = gameOver(gameTurn, choosenBotMovement);
        choosenBotMovement.reset();
      }
      break;
  }
}

int8_t CheckersGame::minmaxAlphaBeta(std::shared_ptr<GameStatus> currentGameState, uint32_t depth, Turn currentTurn, int8_t alpha, int8_t beta){
  if(depth == 0 || gameOver(currentTurn, currentGameState))
    return currentGameState->botTokenCount - currentGameState->humanTokenCount;
  if(currentTurn == Turn::BOT){//MAX
    int8_t maxEvaluation = std::numeric_limits<int8_t>::min();
    while(getNextSimulation(currentTurn, currentGameState)){
      currentGameState->successors.back()->value = minmaxAlphaBeta(currentGameState->successors.back(), depth - 1, Turn::HUMAN, alpha, beta);
      int8_t temp = maxEvaluation;
      maxEvaluation = std::max(currentGameState->successors.back()->value, maxEvaluation);
      if(temp != maxEvaluation && depth == treeDepth){
        choosenBotMovement = currentGameState->successors.back();
      }
      alpha = std::max(alpha, currentGameState->successors.back()->value);
      if(beta <= alpha) break;
    }
    return maxEvaluation;
  }
  else if(currentTurn == Turn::HUMAN){//MIN
    int8_t minEvaluation = std::numeric_limits<int8_t>::max();
    while(getNextSimulation(currentTurn, currentGameState)){
      currentGameState->successors.back()->value = minmaxAlphaBeta(currentGameState->successors.back(), depth - 1, Turn::BOT, alpha, beta);
      minEvaluation = std::min(currentGameState->successors.back()->value, minEvaluation);
      beta = std::min(beta, currentGameState->successors.back()->value);
      if(beta <= alpha) break;
    }
    return minEvaluation;
  }
  return 0;//never happen
}

bool CheckersGame::getNextSimulation(Turn currentTurn, std::shared_ptr<GameStatus> currentGameState){
  if(currentGameState){
    int8_t dy = 0;
    short token = 0;
    switch (currentTurn){
      case Turn::HUMAN:
        token = 1;
        dy = -1;
        break;
      
      case Turn::BOT:
        token = 2;
        dy = 1;
        break;
    }
    bool continueWithSimulation = true;
    for(std::size_t y = currentGameState->auxidy; y < 8; ++y, currentGameState->auxidy = y){
      for(std::size_t x = (continueWithSimulation)?currentGameState->auxidx:0; x < 8; ++x){
        if(currentGameState->mSimulationBoard[y][x] == token){
          Movement moveType;
          if(currentGameState->currentDir2Check == Direction::LEFT){
            currentGameState->currentDir2Check = Direction::RIGHT;
            moveType = validateMovement(currentGameState->mSimulationBoard, currentTurn, sf::Vector2<int8_t>(x,y), sf::Vector2<int8_t>(x - 1, y + dy));
            if(moveType != Movement::ILLEGAL){
              currentGameState->auxidx = x;
              currentGameState->successors.push_back(std::make_shared<GameStatus>(currentGameState->mSimulationBoard));
              confirmMovement(currentGameState->successors.back()->mSimulationBoard, moveType, sf::Vector2<int8_t>(x,y), sf::Vector2<int8_t>(x - 1, y + dy));
              if(moveType == Movement::MURDER){
                if(token == 1)
                  --currentGameState->successors.back()->botTokenCount;
                else
                  --currentGameState->successors.back()->humanTokenCount;
              }
              return true;
            }
            --x;
          }
          else if(currentGameState->currentDir2Check == Direction::RIGHT){
            currentGameState->currentDir2Check = Direction::LEFT;
            moveType = validateMovement(currentGameState->mSimulationBoard, currentTurn, sf::Vector2<int8_t>(x,y), sf::Vector2<int8_t>(x + 1, y + dy));
            if(moveType != Movement::ILLEGAL){
              currentGameState->auxidx = x + 1;
              currentGameState->successors.push_back(std::make_shared<GameStatus>(currentGameState->mSimulationBoard));
              confirmMovement(currentGameState->successors.back()->mSimulationBoard, moveType, sf::Vector2<int8_t>(x,y), sf::Vector2<int8_t>(x + 1, y + dy));
              if(moveType == Movement::MURDER){
                if(token == 1)
                  --currentGameState->successors.back()->botTokenCount;
                else
                  --currentGameState->successors.back()->humanTokenCount;
              }
              return true;
            }
          }
        }
      }
      continueWithSimulation = false;
    }
    currentGameState->auxidy = 8;
  }
  return false;
}

bool CheckersGame::gameOver(Turn currentTurn, std::shared_ptr<GameStatus> currentGameState){
  if(currentGameState != nullptr){
    if(currentGameState->humanTokenCount == 0 || currentGameState->botTokenCount == 0)
      return true;
    bool somethingToDoH = false;
    bool somethingToDoB = false;
    std::size_t maxHumanY = 0 , minBotY = 8;
    for(std::size_t y = 0; y < 8; ++y)
      for(std::size_t x = 0; x < 8; ++x){
        if(currentGameState->mSimulationBoard[y][x] == 1){
          maxHumanY = std::max(maxHumanY, y);
          somethingToDoH = somethingToDoH || (validateMovement(currentGameState->mSimulationBoard, Turn::HUMAN, sf::Vector2<int8_t>(x,y), sf::Vector2<int8_t>(x - 1, y - 1)) != Movement::ILLEGAL);
          somethingToDoH = somethingToDoH || (validateMovement(currentGameState->mSimulationBoard, Turn::HUMAN, sf::Vector2<int8_t>(x,y), sf::Vector2<int8_t>(x + 1, y - 1)) != Movement::ILLEGAL);
        }
        else if(currentGameState->mSimulationBoard[y][x] == 2){
          minBotY = std::min(minBotY, y);
          somethingToDoB = somethingToDoB || (validateMovement(currentGameState->mSimulationBoard, Turn::BOT, sf::Vector2<int8_t>(x,y), sf::Vector2<int8_t>(x - 1, y + 1)) != Movement::ILLEGAL);
          somethingToDoB = somethingToDoB || (validateMovement(currentGameState->mSimulationBoard, Turn::BOT, sf::Vector2<int8_t>(x,y), sf::Vector2<int8_t>(x + 1, y + 1)) != Movement::ILLEGAL);
        }
      }
    if(minBotY < maxHumanY && ((currentTurn == Turn::HUMAN && somethingToDoH) || (currentTurn == Turn::BOT && somethingToDoB)))
      return false;
    return true;
  }
  return false;
}

void CheckersGame::start(){
  std::cout << "+-----------------------------------------+\n";
  std::cout << "|           CHECKERS GAME CONTROLS        |\n";
  std::cout << "+-----------------------------------------+\n";
  std::cout << "o Mouse Left Click : Select any token of yours(HUMAN -> Red, A.I. -> Black).\n";
  std::cout << "o A and D : Move the selected token in left(A) or right(D) direction.\n";
  std::cout << "o Add(+) and Substract(-) : Increase or decrease the depth of the A.I., the limit is 7 to make safe this game.\n";
  std::cout << "o C : Change starter player for the next game between A.I. and HUMAN.\n";
  std::cout << "o F : Finish the current game.\n";
  std::cout << "o R : Restart the game with the new configurations.\n";
  std::cout << "o Left Key and Right key : Increase or decrease the delay of A.I.'s response.\n";
  std::cout << "o S : Get a window capture saved in ../screenshots.\n";

  sf::RenderWindow app(sf::VideoMode(617,617 + SIZE_HUD), "Checkers Game");
  app.setFramerateLimit(60);

  sf::Event action;
  treeDepth = 1;
  botThinkDelay = sf::seconds(0.5f);

  arialFont.loadFromFile("assets/arial.ttf");
  winnerDisplayed.setFont(arialFont);
  winnerDisplayed.setStyle(sf::Text::Bold);
  winnerDisplayed.setCharacterSize(60);
  winnerDisplayed.setOutlineThickness(5);
  winnerDisplayed.setOutlineColor(sf::Color::Black);

  hudDisplayedInfo.setFont(arialFont);
  hudDisplayedInfo.setStyle(sf::Text::Bold);
  hudDisplayedInfo.setCharacterSize(22);
  hudDisplayedInfo.setFillColor(sf::Color(50,255,50));
  hudDisplayedInfo.setOrigin(-5.f, -5.f);
  hudDisplayedInfo.setPosition(0.f, 617.f);

  board.loadFromFile("assets/Board.jpg");
  tokenTexture.loadFromFile("assets/CheckersToken.png");
  sf::Sprite displayableBoard; displayableBoard.setTexture(board);
  displayableBoard.setScale(app.getSize().x / displayableBoard.getGlobalBounds().getSize().x,
                            (app.getSize().y - SIZE_HUD) / displayableBoard.getGlobalBounds().getSize().y);
  
  setInitialPositions();

  while(app.isOpen()){
    app.clear();
    app.draw(displayableBoard);
    displayGame(app);
    if(gameFinished){
      if(int(botTokenCount) == int(humanTokenCount)){
        winnerDisplayed.setFillColor(sf::Color::Cyan);
        winnerDisplayed.setString("Tie");
      }
      else if(int(botTokenCount) > int(humanTokenCount)){
        winnerDisplayed.setFillColor(sf::Color(255, 50, 50));
        winnerDisplayed.setString("A.I. Wins!!!");
      }
      else if(int(botTokenCount) < int(humanTokenCount)){
        winnerDisplayed.setFillColor(sf::Color::Green);
        winnerDisplayed.setString("Human Wins!!!");
      }
      winnerDisplayed.setOrigin(winnerDisplayed.getGlobalBounds().getSize().x/2, winnerDisplayed.getGlobalBounds().getSize().y/2);
      winnerDisplayed.setPosition(308.5, 308.5);
      app.draw(winnerDisplayed);
    }
    else{
      onControlsUpdate(app);
    }
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Left)){
      botThinkDelay = sf::seconds(botThinkDelay.asSeconds() - 0.01);
    }
    else if(sf::Keyboard::isKeyPressed(sf::Keyboard::Right)){
      botThinkDelay = sf::seconds(botThinkDelay.asSeconds() + 0.01);
    }
    displayHUDInfo(app);
    app.display();
    while(app.pollEvent(action)){
      if(action.type == sf::Event::Closed){
        app.close();
      }
      onHUDControlsUpdate(app, action);
    }
  }
}

}

#endif//API_HPP_

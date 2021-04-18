#ifndef API_HPP_
#define API_HPP_

#include <map>

#include <SFML/Graphics.hpp>

namespace AI{

enum Turn{BOT, HUMAN};

class CheckersGame{
private:
  Turn gameState;
  uint8_t tokenHumanCount, tokenBotCount;
public:
  void start();
};

//#################################################################
//#################################################################
//#################################################################

void CheckersGame::start(){
  sf::RenderWindow app(sf::VideoMode(640,640), "Checkers Game");
  app.setFramerateLimit(60);
  sf::Event action;

  sf::Texture board;
  board.loadFromFile("assets/Board.jpg");
  sf::Sprite displayableBoard; displayableBoard.setTexture(board);
  displayableBoard.setScale(app.getSize().x / displayableBoard.getGlobalBounds().getSize().x,
                            app.getSize().y / displayableBoard.getGlobalBounds().getSize().y);
  while(app.isOpen()){
    while(app.pollEvent(action)){
      if(action.type == sf::Event::Closed){
        app.close();
      }
    }
    app.clear();
    app.draw(displayableBoard);
    app.display();
  }
}

}

#endif//API_HPP_

#ifndef TOKEN_HPP_
#define TOKEN_HPP_

#include <SFML/Graphics.hpp>

namespace AI{

enum Turn{BOT, HUMAN};

struct Token{
private:
  sf::Vector2<int8_t> globalPosition;
  sf::Texture* tokenTexture;
  sf::Sprite tokenBody;
public:
  Token(Turn mode, sf::Texture& texture, const int8_t& posX, const int8_t& posY, float scale = 0.15);
  void display(sf::RenderWindow& window);
  void setOffSet(const float& offSet);
  void changePosition(const int8_t& posX, const int8_t& posY);
  void changePosition(sf::Vector2<int8_t> globalPosition);
  bool checkOverlap(const sf::Vector2i& mousePosition);
  sf::Vector2<int8_t> getGlobalPosition();
};

//#################################################################
//#################################################################
//#################################################################

Token::Token(Turn mode, sf::Texture& texture, const int8_t& posX, const int8_t& posY, float scale){
  tokenTexture = &texture;
  tokenBody.setTexture(*tokenTexture);
  tokenBody.setScale(scale, scale);
  tokenBody.setColor(((mode == HUMAN)?sf::Color::Red:sf::Color(55,55,55)));
  changePosition(posX, posY);
}

void Token::display(sf::RenderWindow& window){
  window.draw(tokenBody);
}

void Token::setOffSet(const float& offSet){
  tokenBody.setOrigin(offSet, offSet);
}

void Token::changePosition(const int8_t& posX, const int8_t& posY){
  globalPosition = sf::Vector2<int8_t>(posX, posY);
  tokenBody.setPosition(posX * tokenBody.getGlobalBounds().width, posY * tokenBody.getGlobalBounds().height);
}

void Token::changePosition(sf::Vector2<int8_t> globalPosition){
  this->globalPosition = globalPosition;
  tokenBody.setPosition(globalPosition.x * tokenBody.getGlobalBounds().width, globalPosition.y * tokenBody.getGlobalBounds().height);
}

bool Token::checkOverlap(const sf::Vector2i& mousePosition){
  return tokenBody.getGlobalBounds().contains(sf::Vector2f(mousePosition));
}

sf::Vector2<int8_t> Token::getGlobalPosition(){
  return globalPosition;
}

}

#endif//TOKEN_HPP_
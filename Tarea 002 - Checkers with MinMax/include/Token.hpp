#ifndef TOKEN_HPP_
#define TOKEN_HPP_

#include <SFML/Graphics.hpp>

namespace AI{

struct Token{
  sf::Vector2<uint8_t> globalPosition;
  sf::Texture* tokenTexture;
  sf::Sprite tokenBody;
};

}

#endif//TOKEN_HPP_
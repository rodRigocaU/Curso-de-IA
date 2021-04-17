#ifndef API_HPP_
#define API_HPP_

#include <SFML/Graphics.hpp>

namespace AI{

enum Turn{BOT, HUMAN};

class CheckersGame{
private:
  Turn gameState;
public:
  void start();
};

}

#endif//API_HPP_

#ifndef PFA_TOOLS_H_
#define PFA_TOOLS_H_

#include <cstdlib>
#include <string>
#include "Settings.h"

static uint8_t view_mode;
static int algstate_idx;

typedef std::vector<std::vector<char>> AlgorithmState;

bool readData(const std::string& filename, std::vector<AlgorithmState>& playlist);

void readPlaylist(std::vector<AlgorithmState>& playlist);

void drawCell(sf::RenderWindow& window, const uint32_t& x, const uint32_t& y, const char& cell);

void drawGrid(sf::RenderWindow& window, AlgorithmState& algstate);

void onCameraControl(sf::View& camera);

void onPlaylistControl(std::vector<AlgorithmState>& playlist);

void onViewModeControl();

#endif//PFA_TOOLS_H_
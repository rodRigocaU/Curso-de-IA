import pygame
from pygame.constants import K_r

class BitMatrixViz:
  def __init__(self, nRows, nCols, maxSize = [100,100]) -> None:
      self.posX = 0
      self.posY = 0
      self.nRows = nRows
      self.nCols = nCols
      self.input = []
      self.blockedKeyboard = True
      for y in range(self.nRows):
        self.input.append([])
        for x in range(self.nCols):
          self.input[y].append(0)
      self.cellSizeX = int(maxSize[0] / nCols)
      self.cellSizeY = int(maxSize[1] / nRows)

  def setPosition(self, x, y):
    self.posX = x
    self.posY = y

  def onUserDisplay(self, screen):
    if pygame.get_init():
      for y in range(self.nRows):
        for x in range(self.nCols):
          color = (0,0,0) if self.input[y][x] == 1 else (255,255,255)
          pygame.draw.rect(screen, color, [self.posX + x * self.cellSizeX, self.posY + y * self.cellSizeY, self.cellSizeX, self.cellSizeY], 0)

  def onUserController(self, event):
    if not self.blockedKeyboard:
      globalPos = pygame.mouse.get_pos()
      localPosX = int(globalPos[0] - self.posX)//self.cellSizeX
      localPosY = int(globalPos[1] - self.posY)//self.cellSizeY
      if localPosX < self.nCols and localPosX >= 0 and localPosY < self.nRows and localPosY >= 0:
        if pygame.mouse.get_pressed()[0]:
          self.input[localPosY][localPosX] = 1
        elif pygame.mouse.get_pressed()[2]:
          self.input[localPosY][localPosX] = 0
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_r:
            for y in range(self.nRows):
              for x in range(self.nCols):
                self.input[y][x] = 0

  def setBlockedKeyboard(self, enabled):
    self.blockedKeyboard = enabled

  def getInput(self):
    input = []
    for row in self.input:
      input += row
    return input
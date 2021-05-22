import pygame

class TextBoxInput:
  def __init__(self, posX, posY, w, h, fontPath, label="", limit = 1) -> None:
    self.posX = posX
    self.posY = posY
    self.letterPos = 0
    self.width = w
    self.height = h
    self.charSize = int(h - int(h*0.35))
    self.charLenght = self.charSize * 0.5
    self.rectViewText = int(limit)*self.charLenght
    self.font = pygame.font.Font(fontPath, self.charSize)
    self.textString = ""
    self.textLabel = label
    self.blockingKeyboardEvent = False
    self.blinkCursor = 0
    self.savedContent = ""

    self.onReturnPress = False

  def getInputText(self):
    return self.savedContent

  def getEnabledKeyboard(self):
    return self.blockingKeyboardEvent

  def getReturnPressed(self):
    temp = self.onReturnPress
    self.onReturnPress = False
    return temp

  def onUserDisplay(self, screen):
    if pygame.get_init():
      pygame.draw.rect(screen, (50,50,50), [self.posX, self.posY, self.width, self.height], 0)
      pygame.draw.rect(screen, (0,0,0), [self.posX + self.height*0.09, self.posY + self.height*0.09, self.width - self.height*0.16, self.height - self.height*0.16], 0)
      color = (0,255,0)if self.rectViewText/self.charLenght != len(self.textString) else (255,150,0)
      renderedText = self.font.render(self.textString[:self.letterPos] + ("|"if self.blinkCursor >= 15 else " ") + self.textString[self.letterPos:], True, color)
      screen.blit(renderedText, (self.posX + self.height*0.09, self.posY + self.height*0.09))
      renderedText = self.font.render(self.textLabel, True, (255,255,255))
      screen.blit(renderedText, (self.posX - renderedText.get_width()*0.5 + self.width * 0.5, self.posY - self.height*0.75))
      if self.blockingKeyboardEvent:
        self.blinkCursor = (self.blinkCursor + 1) % 31
      else:
        self.blinkCursor = 0

  def onUserController(self, event):
    globalPos = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
      if globalPos[0] > self.posX and globalPos[0] < self.posX + self.width and globalPos[1] > self.posY and globalPos[1] < self.posY + self.height:
        self.blockingKeyboardEvent = True
      else:
        self.blockingKeyboardEvent = False
    if self.blockingKeyboardEvent:
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          self.savedContent = self.textString
          self.onReturnPress = True
          self.textString = ""
          self.letterPos = 0
        elif event.key == pygame.K_BACKSPACE:
          self.textString = self.textString[:self.letterPos - 1] + self.textString[self.letterPos:]
          self.letterPos -= 1
        elif event.key == pygame.K_LEFT:
          self.letterPos -= 1
        elif event.key == pygame.K_RIGHT:
          self.letterPos += 1
        elif len(self.textString) < self.rectViewText / self.charLenght:
          self.textString = self.textString[:self.letterPos] + event.unicode + self.textString[self.letterPos:]
          self.letterPos += 1
        if self.letterPos < 0:
          self.letterPos = 0
        if self.letterPos >= len(self.textString):
          self.letterPos = len(self.textString)

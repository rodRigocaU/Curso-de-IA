from PgGadgets.BitMatrixApp import BitMatrixViz
from PgGadgets.TextBoxInput import TextBoxInput

import pygame
import json
from datetime import datetime

class DataFileManagerOut:
  def __init__(self, data_path):
    self.data_path = data_path

  def saveBitListOnFile(self, bit_list, output):
    json_dict = {"Dimensionality":len(bit_list), "Output": output, "InputList":bit_list}
    with open(self.data_path + self.getDate() + ".json", 'w') as json_file:
      json.dump(json_dict, json_file)
      json_file.close()

  def getDate(self):
    textName = "" 
    dateTimeObj = datetime.now()
    for l in str(dateTimeObj):
      if l == ':' or l == ' ' or l == '.':
        textName += '-'
      else:
        textName += l
    return textName

if __name__ == "__main__":
  pygame.init()
  screen = pygame.display.set_mode((500, 600))
  pygame.display.set_caption("OCR Perceptron [Dataset Creator]")

  closed = False
  fps = pygame.time.Clock()

  bitMatrix = BitMatrixViz(8, 6, [300,400])
  bitMatrix.setPosition(100, 60)

  
  textLabel = TextBoxInput(235, 510, 45, 40, "Fonts/arial.ttf", "Etiqueta/Significado", 1)
  
  dataManager = DataFileManagerOut("DATA/")

  while not closed:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        closed = True
      textLabel.onUserController(event)
      bitMatrix.onUserController(event)

    screen.fill((40,45,40))
    bitMatrix.onUserDisplay(screen)
    enabledKeyboard = textLabel.getEnabledKeyboard()
    textLabel.onUserDisplay(screen)
    if textLabel.getReturnPressed():
      dataManager.saveBitListOnFile(bitMatrix.getInput(), textLabel.getInputText())
    bitMatrix.setBlockedKeyboard(enabledKeyboard)
    pygame.display.flip()
    fps.tick(30)
  pygame.quit()
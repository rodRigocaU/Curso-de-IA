from NN.Perceptron import PerceptronLayer
from PgGadgets.BitMatrixApp import BitMatrixViz
from PgGadgets.TextBoxInput import TextBoxInput

import pygame

if __name__ == "__main__":
  pygame.init()
  screen = pygame.display.set_mode((500, 600))
  pygame.display.set_caption("OCR Perceptron [Trainer App]")

  binaryStep = lambda x : 1 if x > 0 else 0

  neuron = PerceptronLayer(48, 10, binaryStep, 0.03)

  neuron.overrideNewNN()

  closed = False
  fps = pygame.time.Clock()

  bitMatrix = BitMatrixViz(8, 6, [300,400])
  bitMatrix.setPosition(100, 120)

  textInputLabels = [TextBoxInput(50, 50, 400, 30, "Fonts/arial.ttf", "Ruta de archivo(Perceptron)", 22),
                     TextBoxInput(235, 550, 35, 30, "Fonts/arial.ttf", "Etiqueta/Significado", 1)]
  
  while not closed:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        closed = True
      for label in textInputLabels:
        label.onUserController(event)
      bitMatrix.onUserController(event)

    screen.fill((40,45,40))
    bitMatrix.onUserDisplay(screen)
    enabledKeyboard = True
    for label in textInputLabels:
      enabledKeyboard = enabledKeyboard and label.getEnabledKeyboard()
      label.onUserDisplay(screen)
    bitMatrix.setBlockedKeyboard(enabledKeyboard)
    pygame.display.flip()
    fps.tick(30)
  pygame.quit()
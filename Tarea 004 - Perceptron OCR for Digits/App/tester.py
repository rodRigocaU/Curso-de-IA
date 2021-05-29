from NN.MultiLayerPerceptron import NeuralNet
from NN.MultiLayerPerceptron import convertInUnderstandableOutput
from PgGadgets.BitMatrixApp import BitMatrixViz
from PgGadgets.TextBoxInput import TextBoxInput

import pygame

if __name__ == "__main__":
  pygame.init()
  screen = pygame.display.set_mode((550, 520))
  pygame.display.set_caption("OCR Perceptron [Perceptron Tester (Multilayer)]")

  closed = False
  fps = pygame.time.Clock()

  bitMatrix = BitMatrixViz(8, 6, [300,400])
  bitMatrix.setPosition(40, 90)

  textLabels = {"InputFile" : TextBoxInput(40, 40, 300, 32, "Fonts/arial.ttf", "Nombre de archivo", 25),
                "PredictBox": TextBoxInput(420, 250, 50, 32, "Fonts/arial.ttf", "<?>", 1)}

  neuralNet = NeuralNet([1,2,1], 1, "tanh", 0.5)
  neuralNet.reset()

  while not closed:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        closed = True
      bitMatrix.onUserController(event)
      for textbox in textLabels.values():
        textbox.onUserController(event)

    screen.fill((40,45,40))
    bitMatrix.onUserDisplay(screen)
    enabledKeyboard = True
    bitMatrix.setBlockedKeyboard(enabledKeyboard)
    for textbox in textLabels.values():
      enabledKeyboard = enabledKeyboard and textbox.getEnabledKeyboard()
      textbox.onUserDisplay(screen)
    bitMatrix.setBlockedKeyboard(enabledKeyboard)
    if textLabels["InputFile"].getReturnPressed():
      name = textLabels["InputFile"].getInputText()
      if neuralNet.loadFromFile("SavedPerceptrons/" + name + ".json"):
        print(">> Successful loading")
        textLabels["InputFile"].editableLabel = ("[" + name + "]")
      else:
        print(">> ERROR: The file doesn\'t exist.")

    if textLabels["PredictBox"].getReturnPressed():
      if textLabels["PredictBox"].getInputText() == "?":
        raw_prediction = neuralNet.predict(bitMatrix.getInput())
        prediction = str(convertInUnderstandableOutput(raw_prediction))
        print(raw_prediction)
        textLabels["PredictBox"].editableLabel = ":[Es un " + prediction + "]"
    pygame.display.flip()
    fps.tick(30)
  pygame.quit()

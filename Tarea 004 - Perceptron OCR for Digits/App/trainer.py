from NN.MultiLayerPerceptron import NeuralNet
from NN.MultiLayerPerceptron import ACTIVATION
import json
import glob
import os
import numpy as np

def help(NN):
  print("train: Train Multilayer Perceptron with data from DATA/ folder")
  print("init : Initialize Multilayer Perceptron")
  print("reset: Reset Multilayer Perceptron to default values")
  print("load : Load Multilayer Perceptron from file")
  print("save : Save Multilayer Perceptron on file")
  print("help : Shows his message")
  return NN

def trainPerceptron(NN):
  dataFiles = []
  for file in glob.iglob("DATA/*.json", recursive=True):
    dataFiles.append(file)
  if len(dataFiles) > 0:
    inputs = []
    outputs = []
    for file in dataFiles:
      with open(file, 'r') as jsonNNSource:
        data = json.load(jsonNNSource)
        if data["Dimensionality"] == NN.inputLayerSize:
          inputs.append(data["InputList"])
          outputs.append([float(data["Output"]) * 0.1])
        else:
          continue
    print("\t>> [Data successfully loaded from DATA/ folder...] ->", len(outputs),"files accepted.")
    iterations = int(input("\t>> #Iterations(LIMIT): "))
    NN.train(np.array(inputs), np.array(outputs), iterations)
    print(">> Training finished")
  else:
    print(">> ERROR: The folder \"DATA/\" is empty(no json file found).")
  return NN

def initPerceptron(NN):
  arch = []
  nLayers = int(input("\t>> #Layers: "))
  for layer in range(nLayers):
    neurons = int(input("\t>> #Neurons in layer#" + str(layer) + " -> "))
    arch.append(neurons)
  params = int(input("\t>> #Parameters in First Layer: "))
  lRatio = float(input("\t>> Learning Ratio: "))
  activation = input("\t>> Activation function: ")
  if(activation in ACTIVATION):
    NN = NeuralNet(arch, params, activation, lRatio)
    NN.reset()
  else:
    print("ERROR: That activation function id is not supported")
  return NN

def resetPerceptron(NN):
  NN.reset()
  print(">> Current M. Perceptron set on default parameters.")
  return NN

def loadPerceptron(NN):
  name = input("\t>> Name of M. Perceptron Info(JSON) file: ")
  print(">> Successful loading")if NN.loadFromFile("SavedPerceptrons/" + name + ".json") else print(">> ERROR: The file doesn\'t exist.")
  return NN

def savePerceptron(NN):
  name = input("\t>> Name of file: ")
  print(">> File: ", name + ".json", "saved on", "SavedPerceptrons/") if NN.saveOnFile("SavedPerceptrons/" + name + ".json") else print(">> ERROR: The M. perceptron hasn\'t been initialized.")
  return NN

if __name__ == "__main__":

  neuralNet = NeuralNet([1,2,1], 1, "tanh", 0.5)

  controlPanel = {"train": trainPerceptron,
                  "init" : initPerceptron,
                  "reset": resetPerceptron,
                  "load" : loadPerceptron,
                  "save" : savePerceptron,
                  "help" : help}
  os.system('cls')
  closed = False
  while(not closed):
    print("<PCSTitle>: {OCR Perceptron [Trainer]}")
    print("-"*40)
    neuralNet.getStatus()
    print("-"*40)
    key = input(">> Write a command: ")
    if key == "exit":
      print("--- PROGRAM FINISHED ---")
      exit(0)
    elif key in controlPanel:
      neuralNet = controlPanel[key](neuralNet)
    else:
      print(">> Comando", key, "desconocido, intente nuevamente.")
    os.system('pause')
    os.system('cls')

  
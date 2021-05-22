from NN.Perceptron import PerceptronLayer
import json
import glob
import os

def help(NN):
  print("train: Train Perceptron with data from DATA/ folder")
  print("init : Initialize Perceptron")
  print("reset: Reset Perceptron to default values")
  print("load : Load Perceptron from file")
  print("save : Save Perceptron on file")
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
        if data["Dimensionality"] == NN.WeightInputs - 1:
          inputs.append(data["InputList"])
          outputs.append(int(data["Output"]))
        else:
          continue
    print("\t>> [Data successfully loaded from DATA/ folder...] ->", len(outputs),"files accepted.")
    iterations = int(input("\t>> #Iterations(LIMIT): "))
    NN.train(inputs, outputs, iterations)
    print(">> Training finished")
    NN.inside()
  else:
    print(">> ERROR: The folder \"DATA/\" is empty(no json file found).")
  return NN

def initPerceptron(NN):
  binaryStep = lambda x : 1 if x > 0 else 0
  params = int(input("\t>> #Parameters: "))
  neurons = int(input("\t>> #Neurons: "))
  lRatio = float(input("\t>> Learning Ratio: "))
  NN = PerceptronLayer(params, neurons, binaryStep, lRatio)
  NN.overrideNewNN()
  return NN

def resetPerceptron(NN):
  NN.overrideNewNN()
  print(">> Current Perceptron set on default parameters.")
  return NN

def loadPerceptron(NN):
  name = input("\t>> Name of Perceptron Weights(JSON) file: ")
  print(">> Successful loading")if NN.loadFromFile("SavedPerceptrons/" + name + ".json") else print(">> ERROR: The file doesn\'t exist.")
  return NN

def savePerceptron(NN):
  name = input("\t>> Name of file: ")
  print(">> File: ", name + ".json", "saved on", "SavedPerceptrons/") if NN.saveOnFile("SavedPerceptrons/" + name + ".json") else print(">> ERROR: The perceptron hasn\'t been initialized.")
  return NN

if __name__ == "__main__":
  binaryStep = lambda x : 1 if x > 0 else 0

  neuralNet = PerceptronLayer(48, 10, binaryStep, 0.03)

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

  
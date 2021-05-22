import numpy as np
import random
import json

class PerceptronLayer:
  def __init__(self, nParameters, nNeurons, fActivation, lRatio) -> None:
      self.weights = []
      self.Activation = fActivation
      self.Neurons = nNeurons
      self.WeightInputs = nParameters + 1
      self.learningRatio = lRatio
      self.initialized = False

  def getStatus(self):
    print(" - Initialized: ", self.initialized)
    if(self.initialized):
      print(" - # Neurons: ", self.Neurons)
      print(" - # Input Parameters: ", len(self.weights[0]) - 1)
      print(" - Learning ratio:", self.learningRatio)

  def overrideNewNN(self):
    for n in range(self.Neurons):
      self.weights.append([])
      for p in range(self.WeightInputs):
        self.weights[n].append(random.uniform(-1,1))
    self.initialized = True

  def loadFromFile(self, file):
    try:
      with open(file, 'r') as jsonNNSource:
        data = json.load(jsonNNSource)
        self.weights = data["Weights"]
        self.Neurons = data["Neurons"]
        self.WeightInputs = data["Parameters+Bias"]
        self.learningRatio = data["Learning_Ratio"]
        self.initialized = data["Initialized"]
        jsonNNSource.close()
      return True
    except:
      return False

  def saveOnFile(self, file):
    if self.initialized:
      jsonNNSource = {
        "Weights" : self.weights,
        "Neurons" : self.Neurons,
        "Parameters+Bias" : self.WeightInputs,
        "Learning_Ratio" : self.learningRatio,
        "Initialized" : self.initialized
      }
      with open(file, 'w') as json_file:
        json.dump(jsonNNSource, json_file, indent = 4, sort_keys = True)
        json_file.close()
      return True
    return False
  
  def calculate(self, input):
    if self.initialized:
      output = []
      for n in range(len(self.weights)):
        output.append(self.Activation(float(np.matrix(input + [1]) * np.matrix(self.weights[n]).T)))
      return output
    print("<Error>: Empty Neural Network, use overrideNewNN() or loadFromFile(file)")
    exit(1)
 
  def fit(self, input, output):
    def vec2Num(vec):
      value = 0
      for idx, bit in enumerate(vec):
        value += bit * 2**(len(vec) - 1 - idx)
      return value
    if(len(input) == len(self.weights[0]) - 1):
      obtained = vec2Num(self.calculate(input))
      print("Obtained:", obtained, " Estimated:", output)
      if(obtained != output):
        temp = input + [1]
        for n in range(len(self.weights)):
          for i in range(len(self.weights[n])):
            self.weights[n][i] = self.weights[n][i] + self.learningRatio * temp[i] * (output - obtained)
          print(self.weights[n])
        print("="*40)
        return False
      else:
        return True
    return False

  def inside(self):
    for n in range(len(self.weights)):
      print("- Weight Neuron#" + str(n + 1), ":", self.weights[n])

  def train(self, inputs, outputs, iterations):
    if self.initialized:
      status = False
      while(status != True and iterations != 0):
        status = True
        iterations -= 1
        for i in range(len(inputs)):
          status = status and self.fit(inputs[i], outputs[i])
      return
    print("<Error>: Empty Neural Network, use overrideNewNN() or loadFromFile(file)")
    exit(1)
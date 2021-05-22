import numpy as np
import random

class PerceptronLayer:
  def __init__(self, nParameters, nNeurons, fActivation, lRatio) -> None:
      self.weights = []
      self.Activation = fActivation
      self.Neurons = nNeurons
      self.WeightInputs = nParameters + 1
      self.learningRatio = lRatio
      self.initialized = False

  def overrideNewNN(self):
    for n in range(self.Neurons):
      self.weights.append([])
      for p in range(self.WeightInputs):
        self.weights[n].append(random.uniform(-1,1))
    self.initialized = True

  def loadFromFile(self, filePath):
    self.initialized = True

  def saveOnFile(self, filePath):
    pass
  
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
        print("------------------------------------------------")
        return False
      else:
        return True
    return False

  def inside(self):
    for n in range(len(self.weights)):
      print("- Weight X" + str(n), ":", self.weights[n])

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
import numpy as np
import json
from progress.bar import ChargingBar

E = 2.718281828459045235360
BARSIZE = 100

ACTIVATION = {
  "sigmoid" : [lambda x : 1 / (1 + E ** (-x)), lambda x : x * (1 - x)],
  "relu"    : [lambda x : np.maximum(x, 0), lambda x : (x > 0)],
  "tanh"    : [lambda x : np.tanh(x), lambda x : 1 - np.tanh(x) ** 2]
}

class NeuralLayer:
  def __init__(self, nInput, nNeurons, act_fun, d_act_fun) -> None:
    self.W = np.random.rand(nInput, nNeurons) * 2 - 1
    self.B = np.random.rand(1, nNeurons) * 2 - 1
    self.deltas = np.zeros(self.B.shape)
    self.act_fun = act_fun
    self.d_act_fun = d_act_fun

  def setWeights(self, W, B):
    self.W = W
    self.B = B

  def feedForward(self, X):
    return self.act_fun(X @ self.W + self.B)

  def keepBackward(self, deltasNextLayer, W, a):
    self.deltas =  (deltasNextLayer @ W.T) * self.d_act_fun(a)
    return self.deltas

  def beginBackProp(self, a, Y):
    self.deltas = (a - Y) * self.d_act_fun(a)
    return self.deltas

  def updateWeights(self, X, lRatio):
    self.W -= (X.T @ self.deltas) * lRatio
    self.B -= np.mean(self.deltas, axis=0, keepdims=True) * lRatio
    self.deltas = np.zeros(self.B.shape)

class NeuralNet:
  def __init__(self, topology, nInitInput, act_fun, lRatio) -> None:
    self.act_fun_id = act_fun
    self.act_fun = ACTIVATION[act_fun][0]
    self.d_act_fun = ACTIVATION[act_fun][1]
    self.cost_fun = lambda nnAns, realAns : np.mean((nnAns - realAns)**2)
    self.lRatio = lRatio
    self.network = []
    self.initialized = False
    self.trainingStatus = "0.0 TE"
    self.topology = topology
    self.inputLayerSize = nInitInput

  def getStatus(self):
    print(" - Initialized: ", self.initialized)
    if(self.initialized):
      print(" - # Topology: ", self.topology)
      print(" - Activation Function(ID): ", self.act_fun_id)
      print(" - # Input Parameters: ", self.inputLayerSize)
      print(" - Learning ratio:", self.lRatio)
      print(" - Last training balance: ", self.trainingStatus)

  def loadFromFile(self, file):
    try:
      with open(file, 'r') as jsonNNSource:
        data = json.load(jsonNNSource)
        self.topology = data["Topology"]
        self.inputLayerSize = data["FirstLayer#Inputs"]
        self.act_fun_id = data["ActivationFunction"]
        self.act_fun = ACTIVATION[data["ActivationFunction"]][0]
        self.d_act_fun = ACTIVATION[data["ActivationFunction"]][1]
        self.reset()
        for idx, layer in enumerate(self.network):
          layer.setWeights(np.array(data["Weights"][idx]), np.array(data["Bias"][idx]))
        self.lRatio = data["LearningRatio"]
        self.initialized = data["Initialized"]
        self.trainingStatus = data["TrainingBalance"]
        jsonNNSource.close()
      return True
    except:
      return False

  def saveOnFile(self, file):
    if self.initialized:
      _allW = []
      _allB = []
      for layer in self.network:
        _allW.append(layer.W.tolist())
        _allB.append(layer.B.tolist())
      jsonNNSource = {
        "Topology" : self.topology,
        "FirstLayer#Inputs" : self.inputLayerSize,
        "ActivationFunction" : self.act_fun_id,
        "LearningRatio" : self.lRatio,
        "Weights" : _allW,
        "Bias" : _allB,
        "Initialized" : self.initialized,
        "TrainingBalance" : self.trainingStatus
      }
      with open(file, 'w') as json_file:
        json.dump(jsonNNSource, json_file, indent = 4, sort_keys = True)
        json_file.close()
      return True
    return False

  def reset(self):
    nConnLastLayer = self.inputLayerSize
    self.network = []
    for layer in self.topology:
      self.network.append(NeuralLayer(nConnLastLayer, layer, self.act_fun, self.d_act_fun))
      nConnLastLayer = layer
    self.initialized = True

  def __backPropagation(self, X, Y):
    deltas = 0
    inputs = [X]
    for layer in self.network:
      inputs.append(layer.feedForward(inputs[-1]))
    for l in reversed(range(len(self.network))):
      if l == len(self.network) - 1:
        deltas = self.network[l].beginBackProp(inputs[l + 1], Y)
      else:
        deltas = self.network[l].keepBackward(deltas, W_nl, inputs[l + 1])
      W_nl = self.network[l].W
      self.network[l].updateWeights(inputs[l], self.lRatio)
    return inputs[-1]

  def predict(self, X):
    lastOutput = X
    if self.initialized:
      for layer in self.network:
        lastOutput = layer.feedForward(lastOutput)
    return lastOutput

  def train(self, inputExamples, expected, iterations=BARSIZE):
    if self.initialized:
      currentIteration = 1
      barIteration = 0
      statusBar = ChargingBar("\x1b[4;36m"+"\t>> Training:", max=BARSIZE)
      interval = int(iterations/BARSIZE) if iterations > 100 else 1
      errorMedia = 0
      statusBar.start()
      while(currentIteration <= iterations):
        errorMedia = 0
        prediction = self.__backPropagation(inputExamples, expected)
        errorMedia = self.cost_fun(prediction, expected)
        currentIteration += 1
        if barIteration % interval == 0:
          statusBar.next()
          barIteration = 0
        barIteration += 1
      while(currentIteration < BARSIZE):
        currentIteration += 1
        statusBar.next()
      statusBar.finish()
      self.trainingStatus = str(round(errorMedia,4)) + "TE"
      print("\x1b[1;33m"+"\t>> Error (Media) Cost: ", round(errorMedia,4))
      print("\x1b[0;37m"+"=-"*35 + "=")
    else:
      print("<Error>: Empty Neural Network, use reset() or loadFromFile(file)")
      exit(1)

#NN -> OUTPUT: 1 dim
def convertInUnderstandableOutput(prediction):
  return round((prediction * 10)[0][0])

# nn = NeuralNet([1,4,1], 2, "tanh", 0.08)
# nn.reset()
# print(nn.predict([0,0]))
# print(nn.predict([1,0]))
# print(nn.predict([0,1]))
# print(nn.predict([1,1]))
# X = np.array([
#         [0,0],
#         [0,1],
#         [1,0],
#         [1,1]
#     ])

# Y = np.array([
#         [1/10],
#         [2/10],
#         [3/10],
#         [4/10]
#     ])

# nn.train(X, Y, 2500)
# print(round((nn.predict([0,0]) * 10)[0][0]))
# print(round((nn.predict([0,1]) * 10)[0][0]))
# print(round((nn.predict([1,0]) * 10)[0][0]))
# print(round((nn.predict([1,1]) * 10)[0][0]))

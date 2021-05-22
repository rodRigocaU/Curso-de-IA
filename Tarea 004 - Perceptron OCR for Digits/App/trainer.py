from NN.Perceptron import PerceptronLayer
import json

if __name__ == "__main__":
  binaryStep = lambda x : 1 if x > 0 else 0

  neuron = PerceptronLayer(48, 10, binaryStep, 0.03)

  neuron.overrideNewNN()

  
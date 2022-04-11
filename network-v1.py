from os.path import exists
import random
import math

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def cost(w,l,input,cor):
    for i in range(len(l[0])):
        l[0][i]=input[i]
    for i in range(len(w)):
        for j in range(len(w[i])):
            sum = 0
            for k in range(len(w[i][j])):
                if k == 0:
                    sum = sum + w[i][j][k]
                else:
                    sum = sum + w[i][j][k] * l[i][k - 1]
            l[i + 1][j] = sigmoid(sum)
    c = 1
    for i in range(len(l[len(l) - 1])):
        c = c + (l[len(l) - 1][i] - cor[i]) * (l[len(l) - 1][i] - cor[i])
    c = c / len(l[len(l) - 1])
    return c

# DATA IMPORT SEQUENCE #

# network configuration
nOfInputs = 0
nOfHidden = 0
nOfOutput = 0
nOfHLayers = 0

weights = []
# 3D list of all weights
layers = []
# 2D list of all neurons in all layers
step = 0.01

pathToFile = 'files/saved_weights.txt'  # path to weights file
pathToResults = 'files/final_weights.txt' # path for saving weights
pathToTraining = 'files/training_data/' # training data path
fileExists = exists(pathToFile)  # boolean if weights file exists

# saved_weights.txt
# number of input neurons
# number of hidden neurons
# number of output neurons
# number of hidden layers
# data

if fileExists:

    # Read weights file
    print("Loading weights file")

    f = open(pathToFile)
    fread = f.readlines()

    nOfInputs = int(fread[0])
    nOfHidden = int(fread[1])
    nOfOutput = int(fread[2])
    nOfHLayers = int(fread[3])

    fread.pop(0)
    fread.pop(0)
    fread.pop(0)
    fread.pop(0)

    # Expanding layers' list with proper dimensions

    il = [0 for x in range(nOfInputs)]
    hl = [0 for x in range(nOfHidden)]
    ol = [0 for x in range(nOfOutput)]
    layers = [il, ol]
    for x in range(nOfHLayers):
        layers.insert(1, hl)

    # print(float(fread[0].split()[0])) #test for calling first weight from file

    # Expanding weights' list and importing weights

    iw = [[float(fread[y].split()[x]) for x in range(nOfInputs+1)] for y in range(nOfHidden)]
    for i in range(nOfHidden):
        fread.pop(0)
    hw = [[float(fread[y].split()[x]) for x in range(nOfHidden+1)] for y in range(nOfHidden)]
    for i in range(nOfHidden):
        fread.pop(0)
    lhw = [[float(fread[y].split()[x]) for x in range(nOfHidden+1)] for y in range(nOfOutput)]
    for i in range(nOfOutput):
        fread.pop(0)

    weights = [iw, lhw]
    for x in range(nOfHLayers - 1):
        weights.insert(1, hw)

    f.close()

else:

    # Create new weights file
    #print("Creating new weights file")
    print("Insert number of inputs, number of neurons per hidden layer, number of outputs and number of hidden layers: ")
    print("WARNING: Test training data is prepared for networks with 2 inputs and 3 outputs!")
    nOfInputs = int(input())
    nOfHidden = int(input())
    nOfOutput = int(input())
    nOfHLayers = int(input())

    f = open(pathToFile, "w")
    f.writelines([str(nOfInputs) + "\n", str(nOfHidden) + "\n", str(nOfOutput) + "\n", str(nOfHLayers) + "\n"])

    il = [0 for x in range(nOfInputs)]
    hl = [0 for x in range(nOfHidden)]
    ol = [0 for x in range(nOfOutput)]
    layers = [il, ol]
    for x in range(nOfHLayers):
        layers.insert(1, hl)

    iw = [[float(random.random()) for x in range(nOfInputs+1)] for y in range(nOfHidden)]
    hw = [[float(random.random()) for x in range(nOfHidden+1)] for y in range(nOfHidden)]
    lhw = [[float(random.random()) for x in range(nOfHidden+1)] for y in range(nOfOutput)]

    weights = [iw, lhw]
    for x in range(nOfHLayers - 1):
        weights.insert(1, hw)

    for i in range(nOfHLayers + 1):
        if i < nOfHLayers:
            for j in range(nOfHidden):
                if i == 0:
                    wline = ""
                    for k in range(nOfInputs+1):
                        wline = wline + str(weights[i][j][k]) + " "
                        #print(weights[i][j][k])
                    f.writelines(wline + "\n")
                else:
                    wline = ""
                    for k in range(nOfHidden+1):
                        wline = wline + str(weights[i][j][k]) + " "
                        #print(weights[i][j][k])
                    f.writelines(wline + "\n")
        else:
            for j in range(nOfOutput):
                wline = ""
                for k in range(nOfHidden+1):
                    wline = wline + str(weights[i][j][k]) + " "
                    #print(weights[i][j][k])
                f.writelines(wline + "\n")

    f.close()

#print(layers)
#print(weights)
# weights[bridge_number][destination][source]

# TRAINING SEQUENCE #

for i in range(2):
    currentPath = pathToTraining + str(i) + ".txt"
    f = open(currentPath)

    input = [float(x) for x in str(f.readline()).split()]
    correct = [float(x) for x in str(f.readline()).split()]

    n=1
    while n<=100:
        for i in range(len(weights)):
            for j in range(len(weights[i])):
                for k in range(len(weights[i][j])):
                    cStart = cost(weights,layers,input,correct)
                    if weights[i][j][k]>=0 and weights[i][j][k]<=1:
                        weights[i][j][k] = weights[i][j][k] + step;
                        cChanged = cost(weights, layers, input, correct)
                        if (cStart > cChanged):
                            pass
                        else:
                            weights[i][j][k] = weights[i][j][k] - 2 * step;
                    elif weights[i][j][k]<0:
                        weights[i][j][k] = 0
                    elif weights[i][j][k]>1:
                        weights[i][j][k] = 1
        print("Epoch",n,": Cost =",cost(weights,layers,input,correct))
        n = n+1
    #print(weights)

# SAVING WEIGHTS SEQUENCE #

f = open(pathToResults, "w")
f.writelines([str(nOfInputs) + "\n", str(nOfHidden) + "\n", str(nOfOutput) + "\n", str(nOfHLayers) + "\n"])
for i in range(nOfHLayers + 1):
    if i < nOfHLayers:
        for j in range(nOfHidden):
            if i == 0:
                wline = ""
                for k in range(nOfInputs + 1):
                    wline = wline + str(weights[i][j][k]) + " "
                    #print(weights[i][j][k])
                f.writelines(wline + "\n")
            else:
                wline = ""
                for k in range(nOfHidden + 1):
                    wline = wline + str(weights[i][j][k]) + " "
                    #print(weights[i][j][k])
                f.writelines(wline + "\n")
    else:
        for j in range(nOfOutput):
            wline = ""
            for k in range(nOfHidden + 1):
                wline = wline + str(weights[i][j][k]) + " "
                #print(weights[i][j][k])
            f.writelines(wline + "\n")
print("Weights saved!")
f.close()

# TESTING SEQUENCE #

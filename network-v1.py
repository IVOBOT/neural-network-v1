from os.path import exists
import random

# DATA IMPORT SEQUENCE #

# network configuration
nOfInputs = 0
nOfHidden = 0
nOfOutput = 0
nOfHLayers = 0

weights = []
# 3D list of all weights
layer = []
# 2D list of all neurons in all layers

pathToFile = 'files/saved_weights.txt'  # path to weights file
fileExists = exists(pathToFile)  # boolean if weights file exists

# saved_weights.txt
# number of input neurons
# number of hidden neurons
# number of output neurons
# number of hidden layers
# data

if fileExists:

    # Read weights file
    print("Reading weights file")

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

    iw = [[float(fread[y].split()[x]) for x in range(nOfInputs)] for y in range(nOfHidden)]
    for i in range(nOfHidden):
        fread.pop(0)
    hw = [[float(fread[y].split()[x]) for x in range(nOfHidden)] for y in range(nOfHidden)]
    for i in range(nOfHidden):
        fread.pop(0)
    lhw = [[float(fread[y].split()[x]) for x in range(nOfHidden)] for y in range(nOfOutput)]
    for i in range(nOfOutput):
        fread.pop(0)

    weights = [iw, lhw]
    for x in range(nOfHLayers - 1):
        weights.insert(1, hw)

    f.close()

else:

    # Create new weights file
    print("Creating new weights file")

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

    iw = [[float(random.random()) for x in range(nOfInputs)] for y in range(nOfHidden)]
    hw = [[float(random.random()) for x in range(nOfHidden)] for y in range(nOfHidden)]
    lhw = [[float(random.random()) for x in range(nOfHidden)] for y in range(nOfOutput)]

    weights = [iw, lhw]
    for x in range(nOfHLayers - 1):
        weights.insert(1, hw)

    for i in range(nOfHLayers + 1):
        if i < nOfHLayers:
            for j in range(nOfHidden):
                if i == 0:
                    wline = ""
                    for k in range(nOfInputs):
                        wline = wline + str(weights[i][j][k]) + " "
                        print(weights[i][j][k])
                    f.writelines(wline + "\n")
                else:
                    wline = ""
                    for k in range(nOfHidden):
                        wline = wline + str(weights[i][j][k]) + " "
                        print(weights[i][j][k])
                    f.writelines(wline + "\n")
        else:
            for j in range(nOfOutput):
                wline = ""
                for k in range(nOfHidden):
                    wline = wline + str(weights[i][j][k]) + " "
                    print(weights[i][j][k])
                f.writelines(wline + "\n")

    f.close()

print(layers)
print(weights)

# TRAINING SEQUENCE #

# SAVING WEIGHTS SEQUENCE #

# TESTING SEQUENCE #

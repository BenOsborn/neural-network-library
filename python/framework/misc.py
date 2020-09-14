from math import exp, tanh, log
from matrix import Matrix
from random import choice

# Activation functions
def sigmoid(x, vals=None, deriv=False):
    if deriv:
        return x*(1-x)
    return 1/(1+exp(-x))

def relu(x, vals=None, deriv=False):
    if deriv:
        return 1 if x > 0 else 0.1
    return max(0.1*x, x)

def softmax(val, vals=None, deriv=False):
    if deriv:
        return val*(1-val)
    vals.flatten()
    vals = vals.returnMatrix()[0]
    return exp(val)/sum([exp(x) for x in vals])
    
# Loss functions
def meanSquared(predicted, actual):
    return predicted-actual

def crossEntropy(predicted, actual):
    # This should not need to be corrected really
    if (predicted == 1): # Fixes python auto rounding to 1
        predicted = 0.99999
    elif (predicted == 0): # Fixes python auto rounding to 0
        predicted = 0.00001
    return -1*(actual/predicted) + (1-actual)/(1-predicted)

# Returns the back errors
def backErrors(activation, errors, predicted):
    shape = predicted.size()

    pred = predicted.flatten().returnMatrix()[0]
    errors  = errors.flatten().returnMatrix()[0]

    mat_partial = [error*activation(pred, deriv=True) for pred, error in zip(pred, errors)]
    newMat = Matrix(arr=mat_partial).reshape(shape[0], shape[1])

    return newMat

def getDifferences(loss, predicted, training):
    shape = training.size()

    pred = predicted.flatten().returnMatrix()[0]
    train = training.flatten().returnMatrix()[0]

    mat_errors = [loss(pred, act) for pred, act in zip(pred, train)]
    newMat = Matrix(arr=mat_errors).reshape(shape[0], shape[1])

    return newMat

# Optimizers
def applyMomentum(p_prev, beta1, gradient):
    p = p_prev*beta1 + (1-beta1)*gradient
    return p

def applyRMS(rms_prev, beta2, gradient):
    rms = rms_prev*beta2 + (1-beta2)*(gradient**2)
    return rms

def applyCorrection(param, beta, iteration):
    corrected = param/(1-beta**iteration)
    return corrected

# If I add other optimizers Im going to have to map the optimizers to have the same imput parameters with 'n=b' notation
def adam(pPrev, rmsPrev, gradients, iteration, beta1=0.9, beta2=0.999, epsilon=10e-8):
    gradRaw = gradients.returnMatrix()
    pPrevRaw = pPrev.returnMatrix()
    rmsPrevRaw = rmsPrev.returnMatrix()
    gradSize = gradients.size()

    pRaw = [] 
    rmsRaw = [] 
    adamRaw = []
    for y in range(gradSize[0]):
        tempArrP = []
        tempArrRMS = []
        tempArrAdam = []
        for x in range(gradSize[1]):
            momentum = applyMomentum(pPrevRaw[y][x], beta1, gradRaw[y][x])
            tempArrP.append(momentum)
            momentumCorrected = applyCorrection(momentum, beta1, iteration)

            rms = applyRMS(rmsPrevRaw[y][x], beta2, gradRaw[y][x]) 
            tempArrRMS.append(rms)
            rmsCorrected = applyCorrection(rms, beta2, iteration)

            adam = momentumCorrected / (rmsCorrected**(0.5) + epsilon) # This must have generated a complex number, why?
            tempArrAdam.append(adam)

        pRaw.append(tempArrP)
        rmsRaw.append(tempArrRMS)
        adamRaw.append(tempArrAdam)

    p = Matrix(arr=pRaw)
    rms = Matrix(arr=rmsRaw)
    adam = Matrix(arr=adamRaw)

    return p, rms, adam
import matrix
from misc import backErrors

class FullyConnected:

    def __init__(self, weight_set, bias_set, activation_func):
        self.weights = weight_set
        self.bias = bias_set
        self.activation_func = activation_func

        self.pWeight = matrix.Matrix(dims=weight_set.size(), init=0)
        self.pBias = matrix.Matrix(dims=bias_set.size(), init=0)
        self.rmsWeight = matrix.Matrix(dims=weight_set.size(), init=0)
        self.rmsBias = matrix.Matrix(dims=bias_set.size(), init=0)
        self.iteration = 0 # This has to be reinited at the start of every training session

    def feedForward(self, inputs, training=False):
        multiplied = matrix.multiplyMatrices(self.weights, inputs)
        out = matrix.add(multiplied, self.bias)

        outCpy = out.clone()
        out = out.applyFunc(lambda x: self.activation_func(x, vals=outCpy)) 

        return out

    # This clears the momentum buffer when new sets need to be trained on the model
    def reinit(self):
        self.pWeight = matrix.Matrix(dims=self.weights.size(), init=0)
        self.pBias = matrix.Matrix(dims=self.bias.size(), init=0)
        self.rmsWeight = matrix.Matrix(dims=self.weights.size(), init=0)
        self.rmsBias = matrix.Matrix(dims=self.bias.size(), init=0)
        self.iteration = 0

    def train(self, input_set, predicted, errors, optimizer, learn_rate=0.5):
        self.iteration += 1

        errors = backErrors(self.activation_func, errors, predicted)

        inputTransposed = matrix.Matrix(arr=input_set.returnMatrix()).transpose()

        w_AdjustmentsRaw = matrix.multiplyMatrices(errors, inputTransposed)

        self.pWeight, self.rmsWeight, w_Adjustments = optimizer(self.pWeight, self.rmsWeight, w_AdjustmentsRaw, self.iteration)
        w_Adjustments = matrix.multiplyScalar(w_Adjustments, learn_rate)
        w_New = matrix.subtract(self.weights, w_Adjustments)
        self.weights = w_New

        self.pBias, self.rmsBias, b_Adjustments = optimizer(self.pBias, self.rmsBias, errors, self.iteration)
        b_Adjustments = matrix.multiplyScalar(errors, learn_rate)
        b_New = matrix.subtract(self.bias, b_Adjustments)
        self.bias = b_New

        transposeWeights = matrix.Matrix(arr=self.weights.returnMatrix()).transpose()

        h_Error = matrix.multiplyMatrices(transposeWeights, errors)
        return h_Error

    def returnNetwork(self):
        return self.weights, self.bias
# Takes the dot product of two input vectors
# This probably isnt necessary for the actual functions
def dot(matrix1, matrix2):
    if ((matrix1.size() != matrix2.size()) or (matrix1.size()[0] != 1)): raise Exception("Dot product failed!")

    mat1 = matrix1.returnMatrix()[0]
    mat2 = matrix2.returnMatrix()[0]

    return sum([val1*val2 for val1, val2 in zip(mat1, mat2)])

# Add 1 to 2
def add(matrix1, matrix2):
    if (matrix1.size() != matrix2.size()): raise Exception(f"Matrices must be same size! Matrix size 1: {matrix1.size()} | Matrix size 2: {matrix2.size()}")

    mat1 = matrix1.returnMatrix()
    mat2 = matrix2.returnMatrix()

    matrixNew = []
    for y in range(matrix1.size()[0]):
        tempArr = []
        for x in range(matrix1.size()[1]):
            val = mat2[y][x] + mat1[y][x]
            tempArr.append(val)
        matrixNew.append(tempArr)

    return Matrix(arr=matrixNew)

# Subtract 1 from 2
def subtract(matrix1, matrix2):
    if (matrix1.size() != matrix2.size()): raise Exception(f"Matrices must be same size! Matrix size 1: {matrix1.size()} | Matrix size 2: {matrix2.size()}")

    mat1 = matrix1.returnMatrix()
    mat2 = matrix2.returnMatrix()

    matrixNew = []
    for y in range(matrix1.size()[0]):
        tempArr = []
        for x in range(matrix1.size()[1]):
            val = mat1[y][x] - mat2[y][x]
            tempArr.append(val)
        matrixNew.append(tempArr)

    return Matrix(arr=matrixNew)

# Returns the scalar multiplication of a matrix and a factor
def multiplyScalar(matrix, factor):
    mat = matrix.returnMatrix()

    newMatrix = []
    for y in range(matrix.size()[0]):
        tempArr = []
        for x in range(matrix.size()[1]):
            val = factor*mat[y][x] 
            tempArr.append(val)
        newMatrix.append(tempArr)

    return Matrix(arr=newMatrix)

# Returns matrix1*matrix2
def multiplyMatrices(matrix1, matrix2):
    if (matrix1.size()[1] != matrix2.size()[0]): raise Exception(f"Matrix 1's columns must be equal length to Matrix 2's Rows! Matrix 1's columns: {matrix1.size()[1]} | Matrix 2's rows: {matrix2.size()[0]}")

    mat1 = matrix1.returnMatrix()
    mat2 = matrix2.returnMatrix()

    matrixNew = []
    for y in range(matrix1.size()[0]):
        tempArr = []
        for x in range(matrix2.size()[1]):
            splicedMat2 = [mat2[i][x] for i in range(matrix2.size()[0])]
            val = sum([val1*val2 for val1, val2 in zip(mat1[y], splicedMat2)])
            tempArr.append(val)
        matrixNew.append(tempArr)

    return Matrix(arr=matrixNew)

# For optimization preallocate the length of the matrices and then add in the values by index
class Matrix:
    def validMatrix(self):
        try:
            self.__matrix[0][0]
        except:
            self.__matrix = [self.__matrix]

    def __init__(self, arr=False, dims=False, init=0):
        if (arr != False):
            self.__matrix = arr
            self.validMatrix()
        elif (dims != False):
            self.__matrix = [[init() for _ in range(dims[1])] for _ in range(dims[0])] # Rows and columns (Rows is the height, colums is the row length)
            self.validMatrix()
        else:
            raise Exception("Matrix requires parameter 'arr' or 'dims'!")

    def print(self):
        for row in self.__matrix:
            print(row)
            
    def flatten(self):
        new_matrix = []
        for row in self.__matrix:
            for val in row:
                new_matrix.append(val)
                
        return Matrix(arr=new_matrix)

    def reshape(self, new_rows, new_cols):
        old_size = self.size()
        if (new_rows*new_cols != old_size[0]*old_size[1]): raise Exception(f"Matrix must have same size! Old rows: {old_size[0]} Old cols: {old_size[1]} | New rows: {new_rows} New cols: {new_cols}")
        self.flatten()
        mat_temp_reversed = self.returnMatrix()[0][::-1]

        matrix_new = []
        for _ in range(new_rows):
            temp_row = []
            for _ in range(new_cols):
                val = mat_temp_reversed.pop()
                temp_row.append(val)
            matrix_new.append(temp_row)

        return Matrix(arr=matrix_new)
    
    def transpose(self):
        new_matrix = [[0 for _ in range(len(self.__matrix))] for _ in range(len(self.__matrix[0]))]

        for y in range(len(self.__matrix)):
            for x in range(len(self.__matrix[0])):
                new_matrix[x][y] = self.__matrix[y][x]

        return Matrix(arr=new_matrix)

    def average(self):
        new_matrix = Matrix(arr=self.__matrix)
        new_matrix.flatten()
        ln = new_matrix.size()[1]
        sm = sum(new_matrix.returnMatrix()[0])
        avg = sm/ln

        return avg

    def clone(self):
        return Matrix(arr=self.__matrix)

    def pad(self, pad_up=0, pad_down=0, pad_left=0, pad_right=0, pad_val=0):
        # I want to create a newly sized array and then for all the indexes in the range I want to shift them over by the horizontal and the vertical
        size = self.size()
        size_rows = size[0]
        size_cols = size[1]

        padded_size_rows = size_rows + pad_down + pad_up
        padded_size_cols = size_cols + pad_left + pad_right

        pad_init = [[pad_val for _ in range(padded_size_cols)] for _ in range(padded_size_rows)]

        unpadded_mat = self.returnMatrix()
        for y in range(size_rows):
            for x in range(size_cols):
                pad_init[y+pad_up][x+pad_left] = unpadded_mat[y][x]

        return Matrix(arr=pad_init)

    def applyFunc(self, func):
        size = self.size()
        rows_num = size[0]
        cols_num = size[1]

        mat = self.returnMatrix()

        for y in range(rows_num):
            for x in range(cols_num):
                mat[y][x] = func(self.__matrix[y][x])

        return Matrix(arr=mat)

    # Rotates the matrix by pi radians
    def rotate(self):
        rowsLen = self.size()[0] 
        tempMat = self.returnMatrix()

        for y in range(rowsLen):
            tempMat[y] = tempMat[y][::-1]
        new_mat = tempMat[::-1]

        return Matrix(arr=new_mat)

    def returnMatrix(self):
        return self.__matrix

    # This will need refactoring
    def size(self):
        return len(self.__matrix), len(self.__matrix[0])

    def cut(self, startRow, endRow, startCol, endCol):
        retMatrix = self.returnMatrix()
        dimRows, dimCols = endRow-startRow, endCol-startCol

        tempMatrix = []
        for row in range(dimRows):
            tempArr = []
            for col in range(dimCols):
                val = retMatrix[startRow+row][startCol+col]
                tempArr.append(val)
            tempMatrix.append(tempArr)

        return Matrix(arr=tempMatrix)
import numpy as np

array1 = np.array([[1,2], [3,4]])
array2 = np.array([[5,6], [7,8]])

ew = np.multiply(array1, array2)
print(ew)

matmul = np.matmul(array1, array2)
print(matmul)

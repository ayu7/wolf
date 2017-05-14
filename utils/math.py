#import math
#import cmath
from collections import Iterable
'''
Operations Included:
- vector addition
- vector subraction
- multiplication of a vector by a scalar
- matrix addition
- matrix subtraction
- multiplication of a matrix by a scalar
- dot product
- row slice
- column slice
- number of rows
- number of columns
- matrix multiplication
- trace
- transpose
- vector Euclidean norm
- complex conjugate of a number
- complex conjugate of a vector
- complex conjugate of a matrix
- conjugate transpose
- Frobenius norm (ie, matrix Euclidean norm)
- first minor of a square matrix
- cofactor of a square matrix
- determinant of a square matrix
- cofactor matrix
- adjoint of a square matrix
- inverse of a square matrix
- identity matrix of size n
- power of a matrix
- system of linear equations solver

Operations Checklist:
- cross product of vectors in 3-space???
- Gaussian elimination
- rank
- eigenvalues, eigenvectors
- Cholesky decomposition
- check for invertibility
- check for full rank

A vector in n-space will be represented as a list of length n of numbers.
A matrix in nxm-space will be represented as a list of length n of lists (each of length m) of numbers. Therefore, the matrix will have n rows and m columns.
A vector is also a column matrix. A matrix with only one row is called a row matrix, and the transpose of a row matrix is a vector. Note that we will not be representing the matrices this way.
'''

# complex_conjugate: Returns the complex conjugate of a number (number).
def complex_conjugate(z):
    return z.real - z.imag*1j if z.imag != 0 else z.real

# v_add: Returns the sum of two vectors (vector).
def v_add(u, v):
    return [x+y for x,y in zip(u,v)] if len(u) == len(v) else "Vectors not of same length."

# v_scalar_mult: Returns the product of a vector multiplied by a scalar (vector).
def v_scalar_mult(c, v):
    return [c*x for x in v] #if isinstance(v, Iterable) else c*v

# v_subtract: Returns the difference between two vectors (vector).
def v_subtract(u, v):
    return v_add(u, v_scalar_mult(-1, v))

# v_norm: Returns the Euclidean norm of a vector (number).
def v_euclidean_norm(v):
    return (sum([x**2 for x in v]))**0.5

#v_conjugate: Returns the complex conjugate of a vector (vector).
def v_conjugate(v):
    return [complex_conjugate(x) for x in v]

# dot: Returns the dot product of two vectors (number).
def dot(u, v):
    return sum([x*y for x,y in zip(u,v)]) if len(u) == len(v) else "Vectors not of same length."

# row: Returns the ith row of matrix A (vector).
def row(i, A):
    return A[i]

# col: Returns the jth column of matrix B (vector).
def col(j, B):
    return [r[j] for r in B] #if isinstance(B, Iterable) else 

# num_rows: Returns the number of rows in a matrix (number).
def num_rows(A):
    return len(A) if isinstance(A, Iterable) else 1

# num_cols: Returns the number of columns in a matrix (number).
def num_cols(A):
    if isinstance(A, Iterable):
        if isinstance(A[0], Iterable):
            return len(A[0])
        else:
            return 1

# m_add: Returns the sum of two matrices of the same size (matrix).
def m_add(A, B):
    return [v_add(u,v) for u,v in zip(A, B)]

# m_scalar_mult: Returns the product of a matrix multiplied by a scalar (matrix).
def m_scalar_mult(c, A):
    return [v_scalar_mult(c, v) for v in A] #if isinstance(A, Iterable) else c*A

# m_subtract: Returns the difference between two matrices (matrix).
def m_subtract(A, B):
    return [v_subtract(u, v) for u,v in zip(A, B)]

# m_mult: Returns the product of two matrices (matrix).
def m_mult(A, B):
    def r(i):
        return [dot(row(i,A), col(j,B)) for j in range(num_cols(B))]
    return [r(i) for i in range(num_rows(A))] if num_cols(A) == num_rows(B) else "Matrices cannot be multiplied."

# trace: Returns the trace of a square matrix (number).
def trace(A):
    return sum(A[i][i] for i in range(num_rows(A))) if num_rows(A) == num_cols(A) else "Matrix isn't square."

# transpose: Returns the transpose of a matrix (matrix).
def transpose(A):
    return [col(i, A) for i in range(num_cols(A))]

# conjugate: Returns the conjugate of a matrix (matrix).
def m_conjugate(A):
    return [v_conjugate(v) for v in A]

# conjugate_transpose: Returns the conjugate transpose of a matrix (matrix).
def conjugate_transpose(A):
    return transpose(m_conjugate(A))

# frobenius: Returns the Frobenius norm of a matrix (number).
def frobenius(A):
    return ((trace(m_mult(A, conjugate_transpose(A)))).real)**0.5

# I: Returns the identity matrix of n-space
def I(n):
   def r(x):
       return [0 if i!=x else 1 for i in range(n)]
   return [r(x) for x in range(n)]

# power: Returns the nth power of a square matrix (matrix)
def power(A, n):
    if n==0:
        return I(num_rows(A))
    else:
        return m_mult(A, power(A, n-1))

# first_minor: Finds the determinant of the matrix resulting from removing the ith row and jth column of a given matrix, thus returning the (i,j) minor of a square matrix (number)
def first_minor(i, j, A):
    def r(j, v):
        return [v[x] for x in range(num_rows(A)) if x != j]
    return det([r(j, A[y]) for y in range(num_rows(A)) if y != i])

# cofactor: Returns the (i,j) cofactor of a square matrix (number).
def cofactor(i, j, A):
    return (-1)**(i+j) * first_minor(i, j, A)

# det: Returns the determinant of a square matrix (number).
def det(A):
    if len(A) != len(A[0]):
        return "Matrix isn't square."
    elif len(A) == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        return sum([A[0][j] * cofactor(0, j, A) for j in range(num_rows(A))])

# cofactor_matrix: Returns the cofactor matrix of a square matrix (matrix).
def cofactor_matrix(A):
    def r(i):
        return [cofactor(i, j, A) for j in range(num_rows(A))]
    return [r(i) for i in range(num_rows(A))]

# adjoint: Returns the adjoint of a square matrix (matrix).
def adjoint(A):
    return transpose(cofactor_matrix(A))

# inverse: Returns the inverse of a square matrix (matrix).
def inverse(A):
    return m_scalar_mult((det(A))**(-1), adjoint(A)) #if isInvertible(A) else "Matrix isn't invertible."

# matrix: Converts a vector into a form that can be multiplied by a matrix
def matrix(v):
    return [[v[0]], [v[1]], [v[2]]]

# vector: Converts a nx1 matrix back into a vector form
def vector(m):
    return [m[0][0], m[1][0], m[2][0]]

# system_solver: Solves Ax=b, where A is a matrix, x is the solution vector, and b is a vector. Returns the solution vector for a system of equations (vector)
def system_solver(A, b):
    return vector(m_mult(inverse(A), matrix(b))) #if isInvertible(A) and fullrank(A) else "Can't solve"
    # should replace with Cholesky decomposition?






#################### TESTING FUNCTIONS ####################

'''
print v_add([1,2,3], [4,5,6]) # should return [5,7,9]

print v_scalar_mult(2.5, [1,2,3]) # should return [2.5, 5.0, 7.5]

print v_subtract([4,5,6], [1,2,3]) # should return [3,3,3]

print dot([1,2,3], [4,5,6]) # should return 4+10+18=32

print row(0, [[1,2,3],[4,5,6]]) # should return [1,2,3]

print col(0, [[1,2,3],[4,5,6]]) # should return [1,4]

print m_add([[1,2,3],[4,5,6]], [[5,6,7],[2,3,4]]) # should return [[6,8,10],[6,8,10]]

print m_scalar_mult(2, [[1,2,3],[4,5,6]]) # should return [[2,4,6],[8,10,12]]

print m_subtract([[5,6,7],[2,3,4]],[[1,2,3],[4,5,6]]) # should return [[4,4,4],[-2,-2,-2]]

print m_mult([[4,-1],[0,5]], [[1,8,0],[6,-2,3]]) # should return [[-2,34,-3],[30,-10,15]]

print trace([[1,2,3],[4,5,6],[7,8,9]]) # should return 1+5+9=15

print transpose([[1,2,3],[4,5,6]]) # should return [[1,4],[2,5],[3,6]]

print v_conjugate([1+2j, 2-3j, 5]) # should return [(1-2j), (2+3j), 5]

print m_conjugate([[1+2j, 2-3j, 5],[4+3j, 6, 4j]]) # should return [[(1-2j), (2+3j), 5],[(4-3j), 6, -4j]]

print conjugate_transpose([[1+2j, 2-3j, 5],[4+3j, 6, 4j]]) # should return [[(1-2j), (4-3j)],[(2+3j), 6],[5, -4j]]

print v_euclidean_norm([1,2,3]) # should return the approximated square root of 14

print frobenius([[1+2j, 2-3j, 5],[4+3j, 6, 4j]]) # should return 10.9545

print frobenius([[1,2,3],[4,5,6]]) # should return 9.5394

print first_minor(1,0, [[1,2,3],[4,5,6],[7,8,9]]) # should return [[2,3],[8,9]]

print cofactor(0,0, [[1,2,3],[4,5,6],[7,8,9]]) # should return [[5,6],[8,9]]
print cofactor(0,1, [[1,2,3],[4,5,6],[7,8,9]]) # should return [[-4,-6],[-7,-9]]
print cofactor(0,2, [[1,2,3],[4,5,6],[7,8,9]]) # should return [[4,5],[7,8]]

print det([[1,2],[3,4]]) # should return 4-6=-2

print det([[1,2,3],[4,5,6],[7,8,9]]) # should return 0

print det([[6,1,1],[4,-2,5],[2,8,7]]) # should return -306

print cofactor_matrix([[1,2,3],[4,5,6],[7,8,9]]) # should return [[-3, 6, -3], [6, -12, 6], [-3, 6, -3]]

print adjoint([[1,2,3],[4,5,6],[7,8,9]]) # should return [[-3, 6, -3], [6, -12, 6], [-3, 6, -3]]

print inverse([[1,2,3],[0,1,4],[5,6,0]]) # should return [[-24,18,5],[20,-15,-4],[-5,4,1]]

print m_mult([[1,2,3],[0,1,4],[5,6,0]], [[-24,18,5],[20,-15,-4],[-5,4,1]]) # should return [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

print I(3) # should return [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

print power([[1,-2,3],[5,8,-1],[2,1,1]],3) # should return [[-62,-106,14],[320,344,82],[46,28,28]]

print matrix([9,-5,3])

a = [[1,-2,3],[5,8,-1],[2,1,1]]

print det(a) # should return -10

x = (det(a))**(-1)
print x

print adjoint(a) 

print m_scalar_mult(float(1/det(a)), adjoint(a))

print inverse([[1,-2,3],[5,8,-1],[2,1,1]]) # should return [[-0.9, 0.5, 2.2],[0.7, 0.5, -1.6],[1.1, 0.5, -1.8]]

print system_solver([[1,-2,3],[5,8,-1],[2,1,1]], [9,-5,3]) # should return [1,-1,2]

'''
a = [[1,3,1,9],[1,1,-1,1],[3,11,5,35]]
#print gauss(a) # should return [[1,0,-2,-3],[0,1,1,4],[0,0,0,0]]

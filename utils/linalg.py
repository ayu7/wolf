#import math
import cmath
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
- matrix multiplication
- trace
- transpose
- vector Euclidean norm
- complex conjugate of a vector
- complex conjugate of a matrix
- conjugate transpose
- Frobenius norm (ie, matrix Euclidean norm)
- determinant of a square matrix
- cofactor matrix
- adjoint of a square matrix
- inverse of a square matrix
- power of a matrix
- system of linear equations solver
- Gaussian elimination
- rank
- check for invertibility
- check for Hermitian matrix
- nullity of a matrix
- basis of a rowspace of a matrix
- basis of a columnspace of a matrix
- basis of a nullspace of a matrix

Operations Checklist:
- linear independence of matrix
- eigenvalues, eigenvectors
- characteristic polynomial
- diagonalize a matrix
- LU decomposition
- SVD 

A vector in n-space will be represented as a list of length n of numbers.
A matrix in nxm-space will be represented as a list of length n of lists (each of length m) of numbers. Therefore, the matrix will have n rows and m columns.
A vector is also a column matrix. A matrix with only one row is called a row matrix, and the transpose of a row matrix is a vector. Note that we will not be representing the matrices this way.
'''

# nullity: Returns the nullity of a matrix (number).
def nullity(A):
    return num_cols(A) - rank(A)

# basis_rowspace: Returns the basis of a rowspace of a matrix (matrix -- note: each of the rows in the returned matrix represent the vectors in the set of vectors that is the basis).
def basis_rowspace(A):
    B = gauss(A)
    return [x for x in A if not(is_zero_row(x))]

# basis_columnspace: Returns the basis of a columnspace of a matrix (matrix -- note: each of the rows in the returned matrix represent the vectors in the set of vectors that is the basis).
def basis_columnspace(A):
    return basis_rowspace(transpose(A))

# basis_nullspace: Returns the basis of the nullspace of a matrix (matrix -- note: each of the rows in the returned matrix represent the vectors in the set of vectors that is the basis).
def basis_nullspace(A):
    b = [0 for x in A]
    return system_solver(A, b)

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
    print "DFASDFASDF LINALG SUBTRACT VECTORS"
    print u
    print v
    print v_add(u, v_scalar_mult(-1,v))
    print "DSFASDFASDF END"
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

# is_invertible: Returns true if given square matrix is invertible (boolean).
def is_invertible(A):
    return det(A) != 0 if num_rows(A) == num_cols(A) else "Matrix isn't square"

# is_right_invertible: Returns true if a given matrix has a right inverse (boolean).
def is_right_invertible(A):
    return rank(A) == num_rows(A)

# is_left_invertible: Returns true if a given matrix has a left inverse (boolean).
def is_left_invertible(A):
    return rank(A) == num_cols(A)

# inverse: Returns the inverse of a square matrix (matrix).
def inverse(A):
    return m_scalar_mult((det(A))**(-1), adjoint(A)) if is_invertible(A) else "Matrix isn't invertible."

# matrix: Converts a vector into a form that can be multiplied by a matrix
def matrix(v):
    return [[x] for x in v]

# vector: Converts a nx1 matrix back into a vector form
def vector(m):
    return [x[0] for x in m]

# system_solver: Solves Ax=b, where A is a matrix, x is the solution vector, and b is a vector. Returns the solution vector for a system of equations (vector)
def system_solver(A, b):
    return vector(m_mult(inverse(A), matrix(b))) if is_invertible(A) else "No unique solution"


# argmax: Returns the index of the maximum element in an iterable, checking from indices k to m, f being the function that determines the function to apply to each element.
def argmax(iterable, k, m, f):
   return iterable.index(max(iterable[k:m], key=f))

# swap: Given a matrix and two rows, swaps two rows in the matrix. Returns the matrix.
def swap(A, r1, r2):
    temp = A[r2]
    A[r2] = A[r1][:]
    A[r1] = temp[:]
    return A

# gauss: Gaussian elimination algorithm. Reduces a matrix to row echelon form. Returns the matrix.
def gauss(A):
    m = num_rows(A)
    n = num_cols(A)
    for k in range(min(m,n)): # going through columns, unless there aren't enough rows.
        # checking to make sure that there isn't a whole column of zeroes
        #print A
        c = col(k,A)
        #print "c: " + str(c)
        imax = argmax(c, k, m, abs)
        #print "imax: " + str(imax)
        if A[imax][k] == 0:
            #print A
            #print "s"
            return A
        swap(A, k, imax) # to make sure that in the column and row we want there's a non-zero value
        #print A
        if A[k][k] < 0:
            A[k] = v_scalar_mult(-1, A[k])
        d = 1 / float(A[k][k])
        A[k] = v_scalar_mult(d, A[k]) # now we have our 1
        # iterate through the other rows to cancel out the numbers in the kth column
        for j in range(m):
            if j != k:
                A[j] = v_add(A[j], v_scalar_mult(-A[j][k], A[k]))
    return A

# zero_rows: Given a row of a matrix, returns true if all of the elements are zero (boolean).
def is_zero_row(r):
    return len(list(filter(lambda x:x!=0, r))) == 0

# rank: Given a matrix, returns its rank (the number of non-zero rows in reduce row echelon form) (number).
def rank(A):
    a = gauss(A)
    return num_rows(a) - len(list(filter(is_zero_row, a)))

# full_rank: Given a matrix, returns true if it has full rank (rank = 0) (boolean).
def full_rank(A):
    return rank(A) == 0

# is_hermitian: Returns true if a given matrix is Hermitian (boolean).
def is_hermitian(A):
    return A == conjugate_transpose(A) if num_rows(A) == num_cols(A) else "Matrix not square"

#################### TESTING FUNCTIONS ####################

'''
x1 = 2+1j
x2 = 2-1j
x3 = 1j
x4 = -1j
a = [[2, x1, 4],[x2, 3, x3,],[4, x4, 1]]
print a
print is_hermitian(a)

print is_zero_row([0,0,0,0])
print is_zero_row([0,1,0,0])
a = [[1,3,1,9],[1,1,-1,1],[3,11,5,35]]
print rank(a)


a = [[1,3,1,9],[1,1,-1,1],[3,11,5,35]]
gauss(a)
#print a

m =  num_rows(a)
n = num_cols(a)
print m
print n
k = 0
c= col(k,a)
print c
imax = argmax(c, k, m, abs)
print imax
a = swap(a, k, imax)
print a
f = float(a[k+1][k])/a[k][k]
print f
a[k+1][k+1] = a[k+1][k+1] - a[k][k+1] * f
print a

#print gauss(a) # should return [[1,0,-2,-3],[0,1,1,4],[0,0,0,0]]

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

l = [1,2,-3,-4]
print argmax(l, 1, 4, abs)

'''




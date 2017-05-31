from flask import Flask, render_template, url_for, request, redirect
from utils import mathpix, linalg
from werkzeug.utils import secure_filename
import json
import os

UPLOAD_FOLDER = '/utils/images'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

app = Flask(__name__)

# will add all math.py ops later
mathOps = {"v_add" : linalg.v_add,         #         v_add: sum of two vectors (vector)
           "v_subtract" : linalg.v_subtract,    #    v_subtract: difference between two vectors (vector)
           "m_add" : linalg.m_add,         #         m_add: sum of two matrices of the same size (matrix)
           "m_subtract" : linalg.m_subtract,    #    m_subtract: difference between two matrices (matrix)
           "dot"       : linalg.dot,           #           dot: dot product of two vectors (number)
           "v_scalar_mult": linalg.v_scalar_mult, # v_scalar_mult: product of vector and scalar (vector)
           "m_scalar_mult": linalg.m_scalar_mult, # m_scalar_mult: product of matrix and scalar (matrix)
           "trace"     : linalg.trace,         #         trace: trace of a square matrix (number).
           "transpose" : linalg.transpose,     #     transpose: Returns the transpose of a matrix (matrix)
           "v_euclidean_norm": linalg.v_euclidean_norm,    # v_norm: Euclidean norm of a vector (number)
           "v_conjugate": linalg.v_conjugate,   # v_conjugate: complex conjugate of a vector (vector)
           "m_conjugate": linalg.m_conjugate, # m_conjugate: Returns the conjugate of a matrix (matrix)
           "conjugate_transpose": linalg.conjugate_transpose, # conjugate_transpose: Returns the conjugate transpose of a matrix (matrix)
           "frobenius": linalg.frobenius, # frobenius: Returns the Frobenius norm of a matrix (number)
           "det": linalg.det, # det: Returns the determinant of a square matrix (number)
           "cofactor_matrix": linalg.cofactor_matrix, # cofactor_matrix: Returns the cofactor matrix of a square matrix (matrix)
           "adjoint": linalg.adjoint, # adjoint: Returns the adjoint of a square matrix (matrix)
           "inverse": linalg.inverse, # inverse: Returns the inverse of a square matrix (matrix)
           "power": linalg.power, # power: Returns the nth power of a square matrix (matrix)
           "system_solver": linalg.system_solver, # system_solver:  Returns the solution vector for a system of equations (vector)
           "gauss": linalg.gauss, # gauss: Gaussian elimination algorithm. Reduces a matrix to row echelon form
           "rank": linalg.rank, # rank: Given a matrix, returns its rank (the number of non-zero rows in reduce row echelon form) (number)
           "is_left_invertible": linalg.is_left_invertible, # is_left_invertible: Returns true if a given matrix has a left inverse (boolean)
           "is_right_invertible": linalg.is_right_invertible, # is_right_invertible: Returns true if a given matrix has a right inverse (boolean)
           "is_hermitian": linalg.is_hermitian # is_hermitian: Returns true if a given matrix is Hermitian (boolean)
           }

requirements = {"reqScalar" : ["v_scalar_mult","m_scalar_mult","power"],
                "req1Vec" : ["v_euclidean_norm","v_conjugate","v_scalar_mult"],
                "req2Vec" : ["v_add","v_subtract","dot"],
                "req1Mat" : ["trace","transpose","m_conjugate","conjugate_transpose",
                             "frobenius","det","cofactor_matrix","adjoint","inverse","gauss",
                             "rank","is_left_invertible","is_right_invertible",
                             "is_hermitian","m_scalar_mult","power"],
                "req2Mat" : ["m_add","m_subtract"],
                "reqBoth" : ["system_solver"]
                }

@app.route("/")
@app.route("/home")
def index():
    return render_template("home.html")

@app.route("/draw")
def draw():
    return render_template("draw.html")

@app.route("/type")
def type():
    return render_template("type.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/operations")
def operations():
    return render_template("operations.html")

# working:
# - addvector
# - subvector
# - addmatrix
# - submatrix
# - dot
# - scalvector
# - scalmatrix
# - trace
# - transpose
@app.route("/parse", methods=['POST'])
def parse():
    ## Inputs
    print "Inputs"
    print request.form.get("input1")
    input1 = request.form.get("input1")
    print input1
    input2 = request.form.get("input2") # if scalar: converts to [num]
    print input2
    op = request.form.get("operation")
    print op

    
    #mathpix.check(op,input1,input2,requirements)
    input1 = mathpix.matrixConvert(input1)
    input2 = mathpix.matrixConvert(input2)

    ## Outputs
    print "Outputs"
    conv1 = mathpix.arrToMathJax(input1)
    print conv1
    conv2 = mathpix.arrToMathJax(input2)
    print conv2
    result = None

    
    
    if op in requirements["reqScalar"]:
        #if mathpix.check("reqScalar",input1,input2):
        result = mathOps[op](input2[0],input1) # should specify order of inputs (scalar,matrix/vector)
    if op in requirements["req1Vec"]:
        #if mathpix.check("req1Vec",input1,input2):
        result = mathOps[op](input1)
    if op in requirements["req2Vec"]:
        #if mathpix.check("req2Vec",input1,input2):
        result = mathOps[op](input1,input2)
    if op in requirements["req1Mat"]:
        #if mathpix.check("req1Mat",input1,input2):
        result = mathOps[op](input1)
    if op in requirements["req2Mat"]:
        #if mathpix.check("req2Mat",input1,input2):
        result = mathOps[op](input1,input2)
    if op in requirements["reqBoth"]:
        #if mathpix.check("reqBoth",input1,input2):
        result = mathOps[op](input1,input2)

    resultMJx = arrToMathJax(result)
    print resultMJx
    resultLtX = arrToLatex(result)
    print resultLtX

    return render_template("results.html", latex = result)

    #print data
    #print mathpix.latexConvert(data)
    return redirect("/")

# not working, must convert into jpg not png
# mathpix cant read this?
@app.route("/imgProcess", methods=['POST', 'GET'])
def imgProcess():
    content= request.form.get("boxContent")
    content =  content.replace("png","jpg",1)
    retJSON = mathpix.queryURI(content)
    print retJSON
    #latex = retJSON['latex']
    #result = matrixConvert(latex)
    return render_template("results.html", latex=content)

@app.route("/fileProcess", methods=['POST','GET'])
def fileProcess():
    print request.files
    content = request.files.get("input1")
    return redirect("/")

# Turn off before release
if __name__ == "__main__":
    app.run( debug=True );

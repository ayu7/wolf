from flask import Flask, render_template, url_for, request, redirect
from utils import mathpix, linalg
import json

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
           "transpose" : linalg.transpose,     #     transpose: Returns the transpose of a matrix (matrix).
           "v_euclidean_norm": linalg.v_euclidean_norm,    # v_norm: Euclidean norm of a vector (number)
           "v_conjugate": linalg.v_conjugate    # v_conjugate: complex conjugate of a vector (vector)
           "m_conjugate": linalg.m_conjugate
           "conjugate_transpose": linalg.conjugate_transpose
           "frobenius": linalg.frobenius
           "det": linalg.det
           "cofactor_matrix": linalg.cofactor_matrix
           "adjoint": linalg.adjoint
           "inverse": linalg.inverse
           "power": linalg.power
           "system_solver": linalg.system_solver
           "gauss": linalg.gauss
           "rank": linalg.rank
           "is_left_invertible": linalg.is_left_invertible
           "is_right_invertible": linalg.is_right_invertible
           "is_hermitian": linalg.is_hermitian
           }

reqScalar = ["v_scalar_mult","m_scalar_mult"]
req1Vec = ["v_euclidean_norm","v_conjugate"]
req2Vec = ["v_add","v_subtract","dot"]
req1Mat = ["trace","transpose"]
req2Mat = ["m_add","m_subtract"]

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
    input1 = mathpix.matrixConvert(request.form.get("input1"))
    print input1
    input2 = mathpix.matrixConvert(request.form.get("input2"))
    print input2
    op = request.form.get("operation")
    print op

    ## Outputs
    print "Outputs"
    conv1 = mathpix.arrToMathJax(input1)
    print conv1
    conv2 = mathpix.arrToMathJax(input2)
    print conv2
    result = None

    if op in reqScalar:
        result = mathOps[op](input2[0],input1) # should specify order of inputs (scalar,matrix/vector)
    if op in req1Vec:
        result = mathOps[op](input1)
    if op in req2Vec:
        result = mathOps[op](input1,input2)
    if op in req1Mat:
        result = mathOps[op](input1)
    if op in req2Mat:
        result = mathOps[op](input1,input2)

    resultMJx = arrToMathJax(result)
    print resultMJx
    resultLtX = arrToLatex(result)
    print resultLtX

    return render_template("results.html", latex = result)

    #print data
    #print mathpix.latexConvert(data)
    return redirect("/")

@app.route("/imgProcess", methods=['POST', 'GET'])
def imgProcess():
    content= request.form.get("boxContent")
    return render_template("results.html", latex=content)

# Turn off before release
if __name__ == "__main__":
    app.run( debug=True );

from flask import Flask, render_template, url_for, request, redirect
from utils import mathpix, math
import json

app = Flask(__name__)

# will add all math.py ops later
mathOps = {"addvector" : math.v_add,         #         v_add: sum of two vectors (vector)
           "subvector" : math.v_subtract,    #    v_subtract: difference between two vectors (vector)
           "addmatrix" : math.m_add,         #         m_add: sum of two matrices of the same size (matrix)
           "submatrix" : math.m_subtract,    #    m_subtract: difference between two matrices (matrix)
           "dot"       : math.dot,           #           dot: dot product of two vectors (number)
           "scalvector": math.v_scalar_mult, # v_scalar_mult: product of vector and scalar (vector)
           "scalmatrix": math.m_scalar_mult, # m_scalar_mult: product of matrix and scalar (matrix)
           "trace"     : math.trace,         #         trace: trace of a square matrix (number).
           "transpose" : math.transpose,     #     transpose: Returns the transpose of a matrix (matrix).
           "v_euclidean": math.v_euclidean_norm,    # v_norm: Euclidean norm of a vector (number)
           "v_conjugate": math.v_conjugate}    # v_conjugate: complex conjugate of a vector (vector)

reqScalar = ["scalvector","scalmatrix"]
req1Vec = ["v_euclidean","v_conjugate"]
req2Vec = ["addvector","subvector","dot"]
req1Mat = ["trace","transpose"]
req2Mat = ["addmatrix","submatrix"]

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
    input1 = mathpix.matrixConvert(request.form.get("input1"))
    print input1
    input2 = mathpix.matrixConvert(request.form.get("input2"))
    print input2
    op = request.form.get("operation")
    print op

    if op in reqScalar:
        print mathOps[op](input2[0],input1) # should specify order of inputs (scalar,matrix/vector)
    if op in req1Vec:
        print mathOps[op](input1)
    if op in req2Vec:
        print mathOps[op](input1,input2)
    if op in req1Mat:
        print mathOps[op](input1)
    if op in req2Mat:
        print mathOps[op](input1,input2)
    
    #print data
    #print mathpix.latexConvert(data)
    return redirect("/")

# Turn off before release
if __name__ == "__main__":
    app.run( debug=True );

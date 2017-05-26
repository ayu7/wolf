from flask import Flask, render_template, url_for, request, redirect
from utils import mathpix, linalg
import json

app = Flask(__name__)

# will add all math.py ops later
mathOps = {"addvector" : linalg.v_add,         #         v_add: sum of two vectors (vector)
           "subvector" : linalg.v_subtract,    #    v_subtract: difference between two vectors (vector)
           "addmatrix" : linalg.m_add,         #         m_add: sum of two matrices of the same size (matrix)
           "submatrix" : linalg.m_subtract,    #    m_subtract: difference between two matrices (matrix)
           "dot"       : linalg.dot,           #           dot: dot product of two vectors (number)
           "scalvector": linalg.v_scalar_mult, # v_scalar_mult: product of vector and scalar (vector)
           "scalmatrix": linalg.m_scalar_mult, # m_scalar_mult: product of matrix and scalar (matrix)
           "trace"     : linalg.trace,         #         trace: trace of a square matrix (number).
           "transpose" : linalg.transpose,     #     transpose: Returns the transpose of a matrix (matrix).
           "v_euclidean": linalg.v_euclidean_norm,    # v_norm: Euclidean norm of a vector (number)
           "v_conjugate": linalg.v_conjugate}    # v_conjugate: complex conjugate of a vector (vector)

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
        if mathpix.check(op,input1,input2):
            result = mathOps[op](input2[0],input1) # should specify order of inputs (scalar,matrix/vector)
    if op in req1Vec:
        if mathpix.check("req1Vec",input1,input2):
            result = mathOps[op](input1)
    if op in req2Vec:
        if mathpix.check("req2Vec",input1,input2):
            result = mathOps[op](input1,input2)
    if op in req1Mat:
        if mathpix.check("req1Mat",input1,input2):
            result = mathOps[op](input1)
    if op in req2Mat:
        if mathpix.check("req2Mat",input1,input2):
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
    content =  content.replace("png","jpeg",1)
    retJSON = mathpix.queryURI(content)
    print retJSON
    #latex = retJSON['latex']
    #result = matrixConvert(latex)
    return render_template("results.html", latex=content)

# Turn off before release
if __name__ == "__main__":
    app.run( debug=True );

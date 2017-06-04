from flask import Flask, render_template, url_for, request, redirect
from utils import mathpix, linalg
from werkzeug.utils import secure_filename
import json
import os
import urllib3

basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = 'utils/images/'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#print os.path.join(basedir, app.config['UPLOAD_FOLDER'])

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
           "is_hermitian": linalg.is_hermitian, # is_hermitian: Returns true if a given matrix is Hermitian (boolean)
           "m_multiplication" : linalg.m_mult, # m_mult: Returns the product of two matrices (matrix)
}

opTranslation = {"v_add" : "Vector Addition",
                "v_subtract" : "Vector Subtraction",
                "m_add" : "Matrix Addition",
                "m_subtract" : "Matrix Subtraction",
                "dot"       : "Dot Product",
                "v_scalar_mult": "Scalar Multiplication Of A Vector",
                "m_scalar_mult": "Scalar Multiplication Of A Matrix",
                 "m_multiplication" : "Matrix Multiplication",
                "trace"     : "Matrix Trace",
                "transpose" : "Matrix Transpose",
                "v_euclidean_norm": "Vector Euclidean Norm",
                "v_conjugate": "Vector Conjugate",
                "m_conjugate": "Matrix Conjugate",
                "conjugate_transpose": "Conjugate Transpose",
                "frobenius": "Frobenius Norm",
                "det": "Determinant",
                "cofactor_matrix": "Cofactor Matrix",
                "adjoint": "Adjoint",
                "inverse": "Inverse",
                "power": "Power",
                "system_solver": "Solve System",
                "gauss": "Gaussian Elimination",
                "rank": "Rank Of A Matrix",
                "is_left_invertible": "Left Invertible",
                "is_right_invertible": "Right Invertible",
                "is_hermitian": "Is Hermitian"
}

requirements = {"reqScalar" : ["v_scalar_mult","m_scalar_mult","power"],
                "req1Vec" : ["v_euclidean_norm","v_conjugate","v_scalar_mult"],
                "req2Vec" : ["v_add","v_subtract","dot"],
                "req1Mat" : ["trace","transpose","m_conjugate","conjugate_transpose",
                             "frobenius","det","cofactor_matrix","adjoint","inverse","gauss",
                             "rank","is_left_invertible","is_right_invertible",
                             "is_hermitian","m_scalar_mult","power"],
                "req2Mat" : ["m_add","m_subtract","m_multiplication"],
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

def makeVec(input1):
    try:
        if len(input1[0]) == 1:
            return linalg.vector(input1)
        else: # separation of matrices and vectors
            return input1
    except: # if input is a scalar it is not iterable
        return input1

def makeMat(input1):
    try: 
        return linalg.matrix(input1)
    except:
        return input1
    return input1

# try and catch in operateProc filter, kick user to home and implement flash with exception message
def whichScalar(in1,in2):
    if mathpix.isNum(in1):
        return (in1,in2)
    if mathpix.isNum(in2):
        return (in2,in1)
    else:
        raise Exception("neither input is a scalar")

def whichVector(in1,in2):
    try:
        if len(in1[0]) == 1 and len(in2[0]) != 1:
            return (in1,in2)
        elif len(in1[0]) != 1 and len(in2[0]) == 1:
            return (in2,in1)
        else:
            raise Exception("input fields invalid: one must be vec, one must be mat")
    except:
        raise Exception("input fields invalid: one must be vec, one must be mat")

# return dictionary of mathjaxed inputs/outputs/result, result latex code
def operateProc(op,in1,in2,reqDict):
    input1 = None
    input2 = None

    #mathpix.check(op,input1,input2,requirements)
    
    if op in reqDict['req1Vec']+reqDict['req1Mat'] and not op in reqDict['reqScalar']:
        input1 = makeVec(mathpix.matrixConvert(in1))
        input2 = ""

    else:
        input1 = makeVec(mathpix.matrixConvert(in1))
        input2 = makeVec(mathpix.matrixConvert(in2))

    # print input1
    # print input2
        
    dIn1 = mathpix.arrToMathJax(makeMat(input1))
    dIn2 = mathpix.arrToMathJax(makeMat(input2))

    result = None

    if op in reqDict["reqScalar"]:
        scalar = whichScalar(input1,input2)
        result = mathOps[op](scalar[0],scalar[1]) # should specify order of inputs (scalar,matrix/vector)
    if op in reqDict["req1Vec"] and op not in reqDict["reqScalar"]:
        result = mathOps[op](input1)
    if op in reqDict["req2Vec"]:
        result = mathOps[op](input1,input2)
    if op in reqDict["req1Mat"] and op not in reqDict["reqScalar"]:
        result = mathOps[op](input1)
    if op in reqDict["req2Mat"]:
        result = mathOps[op](input1,input2)
    if op in reqDict["reqBoth"]:
        vector = whichVector(input1,input2)
        result = mathOps[op](input1,input2)
        
    def simpleCheck(result):
        try:
            if mathpix.isNum(result[0]):
                return makeMat(result)
        except:
            return result
        return result

    print result
    result = simpleCheck(result)
    print result
    
    dResultM = mathpix.arrToMathJax(result)
    dResultL = mathpix.arrToLatex(result)

    retDict = {"op"     : opTranslation[op],
               "input1" : dIn1,
               "input2" : dIn2,
               "resMJx" : dResultM,
               "resLat" : dResultL
               }

    return retDict
    

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
    print request.form
    input1 = request.form.get("input1")
    print input1
    input2 = request.form.get("input2")
    print input2
    op = request.form.get("operation")
    print op

    retDict = {}
    if mathpix.check(op,input1,input2,requirements):
        retDict = operateProc(op,input1,input2,requirements)
    else:
        return redirect("/")

    print retDict
    # input1 = mathpix.matrixConvert(input1)
    # print "fDFASDFASD input1 converted"
    # input2 = mathpix.matrixConvert(input2)
    # print "fadsfasdf input2 converted"
    # print "adfasdfa"
    # print input1
    # "-----"
    # print input2
    # ## Outputs
    # print "Outputs"
    # conv1 = mathpix.arrToMathJax(input1)
    # print conv1
    # conv2 = mathpix.arrToMathJax(input2)
    # print conv2
    # result = None

    
    
    # if op in requirements["reqScalar"]:
    #     #if mathpix.check("reqScalar",input1,input2):
    #     result = mathOps[op](input2[0],input1) # should specify order of inputs (scalar,matrix/vector)
    # if op in requirements["req1Vec"]:
    #     #if mathpix.check("req1Vec",input1,input2):
    #     result = mathOps[op](input1)
    # if op in requirements["req2Vec"]:
    #     #if mathpix.check("req2Vec",input1,input2):
    #     print "REQ2VEC"
    #     result = mathOps[op](input1,input2)
    # if op in requirements["req1Mat"]:
    #     #if mathpix.check("req1Mat",input1,input2):
    #     result = mathOps[op](input1)
    # if op in requirements["req2Mat"]:
    #     #if mathpix.check("req2Mat",input1,input2):
    #     result = mathOps[op](input1,input2)
    # if op in requirements["reqBoth"]:
    #     #if mathpix.check("reqBoth",input1,input2):
    #     result = mathOps[op](input1,input2)

    # resultMJx = mathpix.arrToMathJax(result)
    # print resultMJx
    # resultLtX = mathpix.arrToLatex(result)
    # print resultLtX

    return render_template("results.html", operation = retDict["op"], input1 = retDict["input1"], input2 = retDict["input2"], result = retDict["resMJx"], latexCode = retDict["resLat"])

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

def allowedFile(fname):
    return '.' in fname and fname.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def saveFile(fileT):
    filename = secure_filename(fileT.filename)
    fileT.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return UPLOAD_FOLDER+filename

@app.route("/fileProcess", methods=['POST','GET'])
def fileProcess():
    urllib3.disable_warnings()
    op = request.form['operation']
    if request.method == 'POST':
        if 'input1' not in request.files or 'input2' not in request.files:
            return redirect("/")
        file1 = request.files['input1']
        file2 = request.files['input2']
        if op in requirements['req1Vec']+requirements['req1Mat'] and op not in requirements['reqScalar']:
            if file1.filename == '':
                return redirect("/")
            if file1 and allowedFile(file1.filename):
                filename = secure_filename(file1.filename)
                fromAppFPath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
                print fromAppFPath
                fromRootFPath = os.path.join(basedir,fromAppFPath)
                print fromRootFPath
                
                file1.save(fromRootFPath)
                ret = mathpix.queryFPath(fromAppFPath)
                os.remove(fromRootFPath)
                print ret
                print ret['latex']
                input1 = mathpix.matrixConvert(ret['latex'])
                if len(input1[0]) == 1:
                    input1 = linalg.vector(input1) # quick and dirty fix, must restructure to make more modular, should go into checker
                    print input1
                result = mathOps[op](input1)
                latex = mathpix.arrToLatex(result)
                print result
                return render_template("results.html",input1=input1,input2="",result=result,latexCode=latex)
        else:
            if file1.filename == '' or file2.filename == '':
                return redirect("/")
            if file1 and file2 and allowedFile(file1.filename) and allowedFile(file2.filename):
                # can be a function
                fname1 = secure_filename(file1.filename)
                fname2 = secure_filename(file2.filename)
                fAppFPath1 = os.path.join(app.config['UPLOAD_FOLDER'],fname1)
                fAppFPath2 = os.path.join(app.config['UPLOAD_FOLDER'],fname2)
                fRootFPath1 = os.path.join(basedir,fAppFPath1)
                fRootFPath2 = os.path.join(basedir,fAppFPath2)

                # can be a function
                file1.save(fRootFPath1)
                file2.save(fRootFPath2)

                # can be a function
                json1 = mathpix.queryFPath(fAppFPath1)
                json2 = mathpix.queryFPath(fAppFPath2)

                # can be a function
                os.remove(fRootFPath1)
                if fname1 != fname2:
                    os.remove(fRootFPath2)

                # can be a function that every math processor uses
                input1 = mathpix.matrixConvert(json1['latex'])
                input2 = mathpix.matrixConvert(json2['latex'])
                if len(input1[0]) == 1:
                    input1 = linalg.vector(input1)
                if len(input2[0]) == 1:
                    input2 = linalg.vector(input2)

                print input1
                print input2
                result = mathOps[op](input1,input2)
                print result
                

    return redirect("/")

# Turn off before release
if __name__ == "__main__":
    app.run( debug=True );

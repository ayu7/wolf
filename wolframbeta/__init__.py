from flask import Flask, render_template, url_for, request, redirect
from utils import mathpix, linalg, mathML
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
        if mathpix.isNum(input1[0]):
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

    print input1
    print input2
    
    dIn1 = mathML.render(makeMat(input1))
    dIn2 = mathML.render(makeMat(input2))

    if input1 == "":
        dIn1 = ""
    if input2 == "":
        dIn2 = ""
        
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
    
    dResultM = mathML.render(result)
    print dResultM
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
        return render_template("type.html",message="Invalid Input")

    return render_template("results.html", operation = retDict["op"], input1 = retDict["input1"], input2 = retDict["input2"], result = retDict["resMJx"], latexCode = retDict["resLat"])


# not working, must convert into jpg not png
# mathpix cant read this?
@app.route("/imgProcess", methods=['POST', 'GET'])
def imgProcess():
    content1 = request.form.get("boxContent")
    content2 = request.form.get("box1Content")
    op = request.form.get("operation")
    # API only takes jpgs
    content1 =  content1.replace("png","jpg",1)
    content1 =  content1.replace("png","jpg",1)
    
    retJSON1 = mathpix.queryURI(content1)
    retJSON2 = mathpix.queryURI(content2)

    print retJSON1
    print retJSON2

    input1 = retJSON1['latex']
    input2 = retJSON2['latex']

    retDict = {}
    if mathpix.check(op,input1,input2,requirements):
        retDict = operateProc(op,input1,input2,requirements)
    else:
        print "redirected"
        return render_template("draw.html",message="Invalid Input")

    return render_template("results.html", operation = retDict["op"], input1 = retDict["input1"], input2 = retDict["input2"], result = retDict["resMJx"], latexCode = retDict["resLat"])

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
    print "Form: \n"
    print request.form
    print "Files: \n"
    print request.files
    print request.method
    if request.method == 'POST':
        if 'input1' not in request.files and 'input2' not in request.files:
            print "did not receive file(s)"
            return render_template("upload.html",message="Did not receive files")
        file1 = request.files['input1']
        file2 = request.files['input2']
        if op in requirements['req1Vec']+requirements['req1Mat'] and op not in requirements['reqScalar']:
            if file1.filename == '':
                print "empty file"
                render_template("upload.html",message="Empty File")
            if file1 and allowedFile(file1.filename):
                filename = secure_filename(file1.filename)
                fromAppFPath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
                print fromAppFPath
                fromRootFPath = os.path.join(basedir,fromAppFPath)
                print fromRootFPath
                
                file1.save(fromRootFPath)
                ret = mathpix.queryFPath(fromRootFPath)
                os.remove(fromRootFPath)

                input1 = ret['latex']
                input2 = ''
                
                retDict = {}
                if mathpix.check(op,input1,input2,requirements):
                    retDict = operateProc(op,input1,input2,requirements)
                else:
                    print "invalid input"
                    return render_template("upload.html",message="Invalid Input")

                return render_template("results.html", operation = retDict["op"], input1 = retDict["input1"], input2 = retDict["input2"], result = retDict["resMJx"], latexCode = retDict["resLat"])
                
                # print ret
                # print ret['latex']
                # input1 = mathpix.matrixConvert(ret['latex'])
                # if len(input1[0]) == 1:
                #     input1 = linalg.vector(input1) # quick and dirty fix, must restructure to make more modular, should go into checker
                #     print input1
                # result = mathOps[op](input1)
                # latex = mathpix.arrToLatex(result)
                # print result
                # return render_template("results.html",input1=input1,input2="",result=result,latexCode=latex)
            else:
                print "invalid: No file1"
                return render_template("upload.html",message="No File1")
            
        else:
            if file1.filename == '' or file2.filename == '':
                print "invalid: No files"
                return render_template("upload.html",message="No Files")
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
                json1 = mathpix.queryFPath(fRootFPath1)
                json2 = mathpix.queryFPath(fRootFPath2)

                input1 = json1['latex']
                input2 = json2['latex']
                
                # can be a function
                os.remove(fRootFPath1)
                if fname1 != fname2:
                    os.remove(fRootFPath2)

                print input1
                print input2
                    
                retDict = {}
                if mathpix.check(op,input1,input2,requirements):
                    print "entered"
                    retDict = operateProc(op,input1,input2,requirements)
                else:
                    print "invalid input"
                    return render_template("upload.html",message="Invalid Input")

                return render_template("results.html", operation = retDict["op"], input1 = retDict["input1"], input2 = retDict["input2"], result = retDict["resMJx"], latexCode = retDict["resLat"])
                
    #print "invalid: get request"
    return render_template("upload.html",message="Invalid POST")

# Turn off before release
if __name__ == "__main__":
    app.run( debug=True );

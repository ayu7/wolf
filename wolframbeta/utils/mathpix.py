#!/usr/bin/env python

import base64
import requests
import json
import linalg
import os
from collections import Iterable

basedir = os.path.abspath(os.path.dirname(__file__))
fromRootFPath = os.path.join(basedir,"utils/keys.txt")


def keyz(x):
    l = open("utils/keys.txt", "r").read().strip().split("\n")
    return l[x]

# submits a query to Mathpix
# takes argument image which is a filepath
def queryFPath(image):
    image_uri = "data:image/jpg;base64," + base64.b64encode(open(image, "rb").read())
    r = requests.post("https://api.mathpix.com/v3/latex",
                      data=json.dumps({'url': image_uri}),
                      headers={"app_id": keyz(0), "app_key": keyz(1),
                               "Content-type": "application/json"})
    return json.loads(r.text)

#queryFPath("testImages/vec1.jpg")

def queryURI(image):
    r = requests.post("https://api.mathpix.com/v3/latex",
                      data=json.dumps({'url': image}),
                      headers={"app_id": keyz(0), "app_key": keyz(1),
                               "Content-type": "application/json"})
    return json.loads(r.text)

################################################
# Checks/Returns if 'a' is convertible to float
def isNum(a):
    try:
        float(a)
        return True
    except:
        return False
    
def isComplex(string):
    try:
        if ("+" in string or "-" in string) and "i" in string:
            s = string.replace("i","")
            if "+" in string:
                s = s.split("+")
            elif "-" in string:
                s = s.split("-")
            else:
                return False
            for i in s:
                if not isNum(i):
                    return False
            return True
    except:
        return False

def makeComplex(string):
    int1 = None
    int2 = None
    s = string
    if "+" in string:
        s = s.split("+")
    elif "-" in string:
        s = s.split("-")
    else:
        raise Exception("passed string is not a complex number")
    for i in s:
        if "i" in i:
            temp = i.replace("i","")
            int2 = float(temp)
        else:
            int1 = float(i)
    return complex(int1,int2)
        
# finds and returns the type of matrix/vector
def findLType(string):
    lTypeSet = [(r"\begin{array}",r"\end{array}"),
                (r"\begin{bmatrix}",r"\end{bmatrix}"),
                (r"\begin{vmatrix}",r"\end{vmatrix}"),
                (r"\begin{Vmatrix}",r"\end{Vmatrix}")]

    for i in lTypeSet:
        try:
            return (string.index(i[0])+len(i[0]),string.index(i[1]))
        except:
            pass
    raise Exception('no matrix/vector here')

# finds length of each row of a matrix or vector based on the row length indicator
def findRLen(string,lType):
    rLenIndic = string[string.index("{"):string.index("}")+1]
    unusedChar = ["{","}"," "]
    count = 0
    checkFor = ""
    checkInit = False
    for i in rLenIndic:
        if i not in unusedChar:
            if checkFor == "":
                checkFor = i
            elif not i == checkFor:
                raise Exception("improper formatting, row length indicators must be uniform")
            count += 1
    return count

# checks if each row matches given row length
def rLenCheck(rlen,mat):
    rLen = rlen
    # print "rLen below ==="
    # print rLen
    # print "mat below ==="
    # print mat
    if len(mat[0]) == 1: # necessary for horizontal to vertical conversion of vectors
        rLen = 1
    for i in mat:
        if not len(i) == rLen:
            raise Exception("improper row length, one of inputs is not numerical or row length indicator is incorrect")

def elemList(string):
    print string
    bracketCase = False
    elemList = []
    elem = ""
    for i in string:
        if bracketCase and i != "}":
            elem += i
        if i == "{":
            bracketCase = True
            elem = ""
        if i == "}":
            bracketCase = False
            elemList.append(elem.strip())
            elem = ""
    return elemList

def addElem(string):
    if isNum(string):
        return float(string)
    elif isComplex(string):
        return makeComplex(string)

# must be flexible enough to parse other input types
# should work with incorrect input
# - "\\\\" in arrays with "\begin{bmatrix}"
# - nonnumerical matrix values
def matrixConvert(s):
    string = s.replace("\n"," ").replace("\r","")
    #print string
    # print "fasdfasdfa matrixconvert"
    # print string
     # print "fasdfasdfad end"
    ret = []
    # example matrix
    # \\left[ \\begin{array} { l l } { 1} & { 0} \\\\ { 0} & { 1} \\end{array} \\right]
    # example vector
    # \\left[ \\begin{array} { l l l } { 1} & { 2} & { 3} \\end{array} \\right]

    if isNum(string):
        return float(string)
    
    lType = findLType(string)
    latex = string[lType[0]:lType[1]]
    #print latex
    rLen = findRLen(latex,lType)

    if r"\\\\" in latex:
        raise Exception('improperly formatted latex, check backslashes/numerical input!')
    if r"\\" not in latex:
        ret = [addElem(x) for x in elemList(latex) if isNum(x) or isComplex(x)]
    else:
        split = latex.split(r"\\")
        ret = [[addElem(x) for x in elemList(i) if isNum(x) or isComplex(x)] for i in latex.split(r"\\")]

    if len(ret):
        # print "checking rlen"
        rLenCheck(rLen,ret)
        return ret
    raise Exception('improperly formatted latex, check backslashes/numerical input!')

#print "1+3i".split("-")
#print matrixConvert(r"\\left[ \begin{bmatrix} { lll } {1+3i} & { 2} & { 3} \\ { 1.55} & { 2} & { 3} \end{bmatrix} \\right]")
#print matrixConvert(r"6")

# takes an array of elements and returns array of strings of those elements
def strConv(arr):
    return [str(i) for i in arr]

# helper to convert a matrix/vector to a string
# specifically the values into proper formatted string
def aToLHelp(arr):
    mat = []
    tempArr = []
    mat = arr
    for i in mat:
        tempArr.append(" { "+"} & { ".join(strConv(i)))
    return r"} \\".join(tempArr)+"} \end{bmatrix}"

# converts matrix/vector into formatted string for mathjax input
def arrToMathJax(matVec):
    if matVec == []:
        return matVec
    if isNum(matVec):
        return matVec
    arr = matVec
    ret = r"\begin{bmatrix} "

    ret += aToLHelp(arr)
    return ret

# converts matrix/vector into formatted string for latex
def arrToLatex(matVec):
    if matVec == []:
        return matVec
    if isNum(matVec):
        return matVec
    arr = matVec
    rlen = len(arr)
    if isinstance(arr[0],Iterable):
        rlen = len(arr[0])
    string = arrToMathJax(arr)
    string = string[:16]+"{"+" l"*rlen+" }"+string[16:]
    return string

#print arrToMathJax(matrixConvert(r"\\left[ \\begin{array} { l l l } { 1} & { 2} & { 3} \\end{array} \\right]"))

def processBasic(test):
    try:
        matrixConvert(test)
        return True
    except:
        return False
    return False

def vecTest(test):
    return len(test[0]) == 1 # no need to check all rows, matrixConvert has rlenCheck so all rows are equal length

def matTest(test):
    return len(test[0]) > 1

req = {"reqScalar" : ["v_scalar_mult","m_scalar_mult","power"],
                "req1Vec" : ["v_euclidean_norm","v_conjugate","v_scalar_mult"],
                "req2Vec" : ["v_add","v_subtract","dot"],
                "req1Mat" : ["trace","transpose","m_conjugate","conjugate_transpose",
                             "frobenius","det","cofactor_matrix","adjoint","inverse","gauss",
                             "rank","is_left_invertible","is_right_invertible",
                             "is_hermitian","m_scalar_mult","power"],
                "req2Mat" : ["m_add","m_subtract"],
                "reqBoth" : ["system_solver"]
                }
# pass requirements to check then cross reference to be able to check inputs
# do not filter in app.py rather filter within mathpix.py offload filtering work to mathpix.py
def check1(op,input1,input2,reqDict):
    if op in reqDict["req1Vec"]+reqDict["req1Mat"]:
        if not processBasic(input1):
            return (False,False)
        if op in reqDict["reqScalar"]:
            return (True,True)
        return (True,False)
    else:
        if not processBasic(input1) or not processBasic(input2):
            return (False,False)
        return (True,True)
    raise Exception("Error should not be reached, improper return statements")

def check2(op,input1,input2,reqDict):
    if op in reqDict["reqScalar"]:
        if not isNum(input2) and not isNum(input1):
            return False
    if op in reqDict["req1Vec"]:
        if not vecTest(input1):
            return False
    if op in reqDict["req2Vec"]:
        if not vecTest(input1) or not vecTest(input2):
            return False
    if op in reqDict["req1Mat"]:
        if not matTest(input1):
            return False
    if op in reqDict["req2Mat"]:
        if not matTest(input1) or not matTest(input2):
            return False
    if op in reqDict["reqBoth"]:
        if (not matTest(input1) or not vecTest(input2)) and (not vecTest(input1) or not matTest(input2)):
            return False
    return True

def check(op,input1,input2,reqDict):
    initT = check1(op,input1,input2,reqDict)
    print "pass check1"
    arr1 = None
    arr2 = None
    if initT[0] or initT[1]:
        if initT[0]:
            arr1 = matrixConvert(input1)
        if initT[1]:
            arr2 = matrixConvert(input2)
    else:
        return False
    if not check2(op,arr1,arr2,reqDict):
        return False
    return True

#print check("v_conjugate",r"\begin{bmatrix} { lll } { 1} & { 2} & { 3} \end{bmatrix}","",req)
# uncomment requests import!!!

################################################

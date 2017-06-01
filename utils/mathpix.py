#!/usr/bin/env python

import base64
import requests
import json
import linalg
from collections import Iterable

# submits a query to Mathpix
# takes argument image which is a filepath
def queryFPath(image):
    image_uri = "data:image/jpg;base64," + base64.b64encode(open(image, "rb").read())
    r = requests.post("https://api.mathpix.com/v3/latex",
                      data=json.dumps({'url': image_uri}),
                      headers={"app_id": "test", "app_key": "thisisnotourkey",
                               "Content-type": "application/json"})
    return json.loads(r.text)

#queryFPath("testImages/vec1.jpg")

def queryURI(image):
    r = requests.post("https://api.mathpix.com/v3/latex",
                      data=json.dumps({'url': image}),
                      headers={"app_id": "test", "app_key": "thisisnotourkey",
                               "Content-type": "application/json"})
    return json.dumps(json.loads(r.text), indent=4, sort_keys=True)

################################################
# Checks/Returns if 'a' is convertible to int
def isInt(a):
    try:
        int(a)
        return True
    except:
        return False

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
    if len(mat[0]) == 1: # necessary for horizontal to vertical conversion of vectors
        rLen = 1
    for i in mat:
        if not len(i) == rLen:
            raise Exception("improper row length, one of inputs is not numerical or row length indicator is incorrect")
    
# must be flexible enough to parse other input types
# should work with incorrect input
# - "\\\\" in arrays with "\begin{bmatrix}"
# - nonnumerical matrix values
def matrixConvert(string):
    ret = []
    # example matrix
    # \\left[ \\begin{array} { l l } { 1} & { 0} \\\\ { 0} & { 1} \\end{array} \\right]
    # example vector
    # \\left[ \\begin{array} { l l l } { 1} & { 2} & { 3} \\end{array} \\right]

    lType = findLType(string)
    latex = string[lType[0]:lType[1]]
    #print latex
    rLen = findRLen(latex,lType)

    # suddenly deprecated, leave this alone for robustness testing if anything changes
    # if "\begin{array}" in latex:
    #     if r"\\" not in latex:
    #         ret = [[int(x)] for x in latex if isInt(x)]
    #     else:
    #         split = latex.split(r"\\")
    #         ret = [[int(x) for x in i if isInt(x)] for i in latex.split(r"\\\\")]
    # else:
        
    if r"\\\\" in latex:
        raise Exception('improperly formatted latex, check backslashes/numerical input!')
    if r"\\" not in latex:
        ret = [[int(x)] for x in latex if isInt(x)]
    else:
        split = latex.split(r"\\")
        ret = [[int(x) for x in i if isInt(x)] for i in latex.split(r"\\")]
            
    if len(ret):
        rLenCheck(rLen,ret)
        return ret
    raise Exception('improperly formatted latex, check backslashes/numerical input!')

#matrixConvert(r"\\left[ \begin{bmatrix} { lll } { 1} & { 2} & { 3} \end{bmatrix} \\right]")

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
    arr = matVec
    ret = r"\begin{bmatrix} "

    ret += aToLHelp(arr)
    return ret

# converts matrix/vector into formatted string for latex
def arrToLatex(matVec):
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
        if not isInt(input2[0]):
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

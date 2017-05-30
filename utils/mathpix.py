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
    print image_uri
    r = requests.post("https://api.mathpix.com/v3/latex",
                      data=json.dumps({'url': image_uri}),
                      headers={"app_id": "efrey", "app_key": "5f578f9e0320da38afcf226cd61b6513",
                               "Content-type": "application/json"})
    return json.dumps(json.loads(r.text), indent=4, sort_keys=True)

#queryFPath("testImages/vec1.jpg")

def queryURI(image):
    r = requests.post("https://api.mathpix.com/v3/latex",
                      data=json.dumps({'url': image}),
                      headers={"app_id": "efrey", "app_key": "5f578f9e0320da38afcf226cd61b6513",
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
    lTypeSet = [(r"\\begin{array}",r"\\end{array}"),
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
    if "\\begin{array}" in latex:
        if r"\\\\" not in latex:
            ret = [[int(x)] for x in latex if isInt(x)]
        else:
            split = latex.split(r"\\\\")
            ret = [[int(x) for x in i if isInt(x)] for i in latex.split(r"\\\\")]
    else:
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
    
def check(cType,input1,input2):
    if cType in ["v_scalar_mult","m_scalar_mult","req1Vec","req1Mat"]:
        if not processBasic(input1):
            return False
    else:
        if not processBasic(input1) or not processBasic(input2):
            return False
    return True



#check("reqVec",r"\begin{bmatrix} { l } { 1} \\ { 2} \\ { 3} \end{bmatrix}","")

################################################


# ################################################
# # finds matrix closest to the beginning of the string
# # returns tuple of strings to look for/slice with
# def findLType(string):
#     closestArr = 9999
#     ret = None
#     TypeSet = [(r"\\begin{array}",r"\\end{array}"),
#                 (r"\begin{bmatrix}",r"\end{bmatrix}"),
#                 (r"\begin{vmatrix}",r"\end{vmatrix}"),
#                 (r"\begin{Vmatrix}",r"\end{Vmatrix}")]

#     for i in TypeSet:
#         try:
#             curInd = string.index(i[0])
#             if curInd < closestArr and curInd >= 0:
#                 closestArr = string.index(i[0])
#                 ret = i
#                 #print ret
#         except:
#             pass
#     return ret


# # all of this is deprecated: get rid of it
# # Works
# # problems of note:
# #  - amount of backslashes is variable, find a way to standardize
# #  - different latex syntax is given from mathpix than recent update
# #     - Mathpix: r"\\begin{array} ... \\end{array}"
# #     - Everyone else: r"\begin{bmatrix} ... \end{bmatrix}"
# #  - sanitation of content of an array:
# #     - This is an array:     r"\\left[ \\begin{array} { l l l } { 1} & { 2} & { 3} \\end{array} \\right]"
# #     - This is not an array: r"\\left[ \\begin{array} not correct content \\end{array} \\right]"
# #     - Current parser cannot tell the difference
# # possible solutions:
# #     - Sanitize/standardize then parse
# #     - Visitor object/function: google this
# #     - Two different functions for mathpix parsing and everyone else parsing

# # Takes string of LaTex matrix or vector, outputs list of matrices in
# def matrixFilter(string):
#     Type = findLType(string) # returns a begin and end string depending on matrix closest to beginning of string
#     try:
#         if(len(string)):
#             return [string[string.index(Type[0]):string.index(Type[1])]] + matrixFilter(string[string.index(Type[1])+len(Type[1]):])
#         else:
#             return []
#     except:
#         return [] # concatenating a None to a list will nullify the list wtf

# # deprecated
# def latexConvert(latex):
#     string = latex
#     matrices = []
#     for i in matrixFilter(string):
#         matrices.append(matrixConvert(i))
#     # utilize switch for operations
#     # cases include different combinations of inputs
#     return matrices

# # string = matrixFilter(r"\\begin{bmatrix}  asdsddgsdfg \\end{bmatrix} \\begin{Vmatrix}  second matrix \\end{Vmatrix}")
# # print string

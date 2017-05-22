#!/usr/bin/env python

import base64
import requests
import json

# submits a query to Mathpix
# takes argument image which is a filepath
def query(image):
    image_uri = "data:image/jpg;base64," + base64.b64encode(open(image, "rb").read())
    r = requests.post("https://api.mathpix.com/v3/latex",
                      data=json.dumps({'url': image_uri}),
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

# must be flexible enough to parse other input types
def matrixConvert(latex):
    # example matrix
    # \\left[ \\begin{array} { l l } { 1} & { 0} \\\\ { 0} & { 1} \\end{array} \\right]
    # example vector
    # \\left[ \\begin{array} { l l l } { 1} & { 2} & { 3} \\end{array} \\right]
   
    # if contains '\\\\': matrix else vector

    if r"\\\\" not in latex:
        return [int(x) for x in latex if isInt(x)]
    else:
        split = latex.split(r"\\\\")
        return [[int(x) for x in i if isInt(x)] for i in latex.split(r"\\\\")]
################################################

################################################
# finds matrix closest to the beginning of the string
# returns tuple of strings to look for/slice with
def findLType(string):
    closestArr = 9999
    ret = None
    lTypeSet = [(r"\\begin{array}",r"\\end{array}"),
                (r"\begin{bmatrix}",r"\end{bmatrix}"),
                (r"\begin{vmatrix}",r"\end{vmatrix}"),
                (r"\begin{Vmatrix}",r"\end{Vmatrix}")]

    for i in lTypeSet:
        try:
            curInd = string.index(i[0])
            if curInd < closestArr and curInd >= 0:
                closestArr = string.index(i[0])
                ret = i
                #print ret
        except:
            pass
    return ret
# Works
# problems of note:
#  - amount of backslashes is variable, find a way to standardize
#  - different latex syntax is given from mathpix than recent update
#     - Mathpix: r"\\begin{array} ... \\end{array}"
#     - Everyone else: r"\begin{bmatrix} ... \end{bmatrix}"
#  - sanitation of content of an array:
#     - This is an array:     r"\\left[ \\begin{array} { l l l } { 1} & { 2} & { 3} \\end{array} \\right]"
#     - This is not an array: r"\\left[ \\begin{array} not correct content \\end{array} \\right]"
#     - Current parser cannot tell the difference
# possible solutions:
#     - Sanitize/standardize then parse
#     - Visitor object/function: google this
#     - Two different functions for mathpix parsing and everyone else parsing

# Takes string of LaTex matrix or vector, outputs list of matrices in 
def matrixFilter(string):
    lType = findLType(string) # returns a begin and end string depending on matrix closest to beginning of string
    try:
        if(len(string)):
            return [string[string.index(lType[0]):string.index(lType[1])]] + matrixFilter(string[string.index(lType[1])+len(lType[1]):])
        else:
            return []
    except:
        return [] # concatenating a None to a list will nullify the list wtf

# deprecated
def latexConvert(latex):
    string = latex
    matrices = []
    for i in matrixFilter(string):
        matrices.append(matrixConvert(i))
    # utilize switch for operations
    # cases include different combinations of inputs
    return matrices

# string = matrixFilter(r"\\begin{bmatrix}  asdsddgsdfg \\end{bmatrix} \\begin{Vmatrix}  second matrix \\end{Vmatrix}")
# print string


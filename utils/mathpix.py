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
            if curInd < closestArr and curInd > 0:
                print i
                closestArr = string.index(r"\\begin{array}")
                ret = i
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
    lType = findLType(string)
    if lType == 1:
        begin = r"\\begin{array}"
        end = r"\\end{array}"
    else:
        begin = r"\begin{bmatrix}"
        end = r"\end{bmatrix}"
    try:
        if(len(string)):
            return [string[string.index(begin):string.index(end)]] + matrixFilter(string[string.index(end)+len(end):])
        else:
            return []
    except:
        return [] # concatenating a None to a list will nullify the list wtf

# deprecated atm
def latexConvert(latex,op):
    string = latex
    parsed = ""
    # utilize switch for operations
    # cases include different combinations of inputs
    return parsed

string = findLType(r"\\begin{array}  asdsddgsdfg \\end{array}")
asdf = r"\\begin{array} mroe stwusdf"
print asdf.index(r"\\begin{array}")
#print string


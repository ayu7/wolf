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

# Broken ATM but on the right track
def matrixFilter(string):
    try:
        return [string[string.index(r"\\begin{array}"):string.index(r"\\end{array}")],matrixFilter(string[string.index(r"\\end{array}"):])]
    except:
        return
   
def latexConvert(latex,op):
    string = latex
    parsed = ""
    # utilize switch for operations
    # cases include different combinations of inputs
    return parsed

string = matrixFilter(r"\\left[ \\begin{array} { l l } { 1} & { 0} \\\\ { 0} & { 1} \\end{array} \\right] \\left[ \\begin{array} { l l } { 1} & { 0} \\\\ { 0} & { 1} \\end{array} \\right]")
print string

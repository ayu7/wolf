from collections import Iterable
def isInt(x):
    try:
        int(x)
        return True
    except:
        return False

def isNum(a):
    try:
        float(a)
        return True
    except:
        return False

def isMat(x):
    return isinstance(x, Iterable)

def generateMatrix(x):
    ret = '<mfenced open="[" close="]"> <mtable>'
    for r in x:
        #print r
        row = "<mtr>"
        for c in r:
            #print c
            col = "<mtd>"
            col += "<mn>" + str(c) + "</mn>"
            col += "</mtd>"
            #print col
            row += col
        row += "</mtr>"
        #print row
        ret += row
    ret += "</mtable></mfenced>"
    return ret

def render(x):
    if isInt(x) or isNum(x):
        return "<mn>"+str(x)+"</mn>"
    elif isMat(x):
        return generateMatrix(x)
    else:
        return "<mtext>"+ str(x) + "</mtext>"

# x = [[1,2,3],[4,5,6],[7,8,9]]
# print render(x)

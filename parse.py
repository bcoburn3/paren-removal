def parsefile(filename):
    res = []
    for line in open(filename):
        res.append(stripstring(line.split(":")[1].strip()))
    print res

def stripstring(str):
    #returns a string which is equivalent to the input string with redundant
    #parens removed
    printtree(parsestring(str))

def parsestring(input):
    #parses a input string into a tree structure representing the input expression
    input = input.replace("**","^")
    input = input.replace("("," ( ")
    input = input.replace(")"," ) ")
    tokens = input.split()
    tree = parselist(tokens)
    return tree

def parselist(tokens):
    #general algorithm:  make a tree, represented as a list where each element
    #is either a number, an operator, or a sub-list representing a parenthesized
    #sub expression.

    # for example, (1 + (2 + 1)) becomes [1, +, [2, +, 1]]

    #then, if a sub expression has the same or higher precedence than the parent,
    #move it up into the higher level list

    #the rules for division and subtraction are a little more complicated, but
    #but not too bad

    res =[]
    i = 0
    while i < len(tokens):
        elem = tokens[i]
        #print(elem)
        #print(i)
        if elem == "(":
            #search forward for the matching close paren
            parencount = 0
            for endidx, elem2 in enumerate(tokens[i:]):
                #print("inner loop")
                #print elem2
                if elem2 == "(":
                    parencount += 1
                elif elem2 == ")":
                    parencount -= 1

                if parencount == 0:
                    #we've found the relevant closing paren, copy this slice into the
                    #result list and update the index
                    sublist = tokens[(i + 1):(endidx + 2)]
                    res.append(parselist(sublist))
                    #print(sublist)
                    i += endidx + 1
                    break
        else:
            res.append(elem)
            i += 1
    return res

print(parsestring("1 + ( 2 + ( 3 + 4 ) )"))
#should print:
#['1', '+', ['2', '+', ['3', '+', '4']]]

def precedence(exp):
    #returns the precendence of the lowest precedence operator in exp
    #exp to be a list or character
    if isinstance(exp, list):
        res = []
        if "+" in exp:
            res.append(1)
        if "-" in exp:
            res.append(1)
        if "*" in exp:
            res.append(2)
        if "/" in exp:
            res.append(2)
        if "^" in exp:
            res.append(3)
        return res
    else:
        if exp == "+":
            return 1
        elif exp == "-":
            return 1
        elif exp == "*":
            return 2
        elif exp == "/":
            return 2
        elif exp == "^":
            return 3

def flipaddition(exp):
    #flips addition and subtraction in exp
    res = []
    for x in exp:
        if x == "+":
            res.append("-")
        elif x == "-":
            res.append("+")
        else:
            res.append(x)
    return res

def flattenlist(exp):
    #takes an expresion represented as a list and recursively flattens it
    test = False
    res = []
    for idx, elem in enumerate(exp):
        if isinstance(elem, list):
            sublist = flattenlist(elem)
            neighbors = []
            if idx != 0:
                neighbors.append(exp[idx - 1])
            if idx != len(exp) - 1:
                neighbors.append(exp[idx + 1])
##            print("flatten test")
##            print(sublist)
##            print(neighbors)
##            print(precedence(sublist))
##            print(precedence(neighbors))
##            print(max(max(precedence(sublist)), max(precedence(neighbors))))
            if min(precedence(sublist)) >= max(precedence(neighbors)):
                #sub-expression can be flattened
                if max(max(precedence(sublist)), max(precedence(neighbors))) == 3:
                    res.append(sublist)
                elif idx != 0:
                    if exp[idx - 1] == "-":
                        #if the sublist is being subtracted, multiply by -1
                        #this is equivalent to switching + and - symbols
                        sublist = flipaddition(sublist)
                        res.extend(sublist)
                    elif exp[idx - 1] == "/":
                        res.append(sublist)
                    else:
                        res.extend(sublist)
                else:
                    res.extend(sublist)
            else:
                #sub-expression can't be flattened, just append as a list
                res.append(sublist)
        else:
            #element isn't a list, so just append it
            res.append(elem)
    return res

print(flattenlist(parsestring("1 + ( 2 + ( 3 + 4 ) )")))
#should print:
#['1', '+', '2', '+', '3', '+', '4']

print(flattenlist(parsestring("1 + ( 2 + ( 3 + 4 ) ) * 5")))
#should print:
#['1', '+', ['2', '+', '3', '+', '4'], '*', '5']

print(flattenlist(parsestring("1 + ( 2 - ( 3 + 4 ) ) * 5")))
#should print:
#['1', '+', ['2', '-', '3', '-', '4'], '*', '5']

print(flattenlist(parsestring("2 ^ ( 3 ^ 4 )")))
#should print:
#['2', '^', ['3', '^', '4']]

def printtree(tree):
    #converts the tree structure into an appropriately parenthesized string
    res = "("
    for elem in tree:
        if isinstance(elem, list):
            res += printtree(elem)
            res += " "
        else:
            res += elem
            res += " "
    #res = res[0:(len(res) - 1)]
    res = res.strip()
    res += ")"
    return res

print(printtree(flattenlist(parsestring("1 + ( 2 + ( 3 + 4 ) ) * 5"))))

parsefile("C:\\temp\\inder.txt")

def parsestring(input):
    #general algorithm:  make a tree, represented as a list where each element
    #is either a number, an operator, or a sub-list representing a parenthesized
    #sub expression.

    # for example, (1 + (2 + 1)) becomes [1, +, [2, +, 1]]

    #then, if a sub expression has the same or higher precedence than the parent,
    #move it up into the higher level list

    #this will require something clever for subtraction and division, tbd later

    tokens = input.split()
    return parselist(tokens)

def parselist(tokens):
    res =[]
    i = 0
    while i < len(tokens):
        elem = tokens[i]
        print(elem)
        print(i)
        if elem == "(":
            #search forward for the matching close paren
            parencount = 0
            for endidx, elem2 in enumerate(tokens[i:]):
                print("inner loop")
                print elem2
                if elem2 == "(":
                    parencount += 1
                elif elem2 == ")":
                    parencount -= 1

                if parencount == 0:
                    #we've found the relevant closing paren, copy this slice into the
                    #result list and update the index
                    sublist = tokens[(i + 1):(endidx + 2)]
                    res.append(parselist(sublist))
                    print(sublist)
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

def flattenlist(exp):
    #takes an expresion represented as a list and recursively flattens it
    last = len(exp) - 1
    test = False
    res = []
    for idx, elem in enumerate(exp):
        if isinstance(elem, list):
            sublist = flattenlist(elem)
            neighbors = []
            if idx != 0:
                neighbors.append(exp[idx - 1])
            if idx != last:
                neighbors.append(exp[idx + 1])
            print("flatten test")
            print(sublist)
            print(neighbors)
            print(precedence(sublist))
            print(precedence(neighbors))
            if min(precedence(sublist)) >= max(precedence(neighbors)):
                #sub-expression can be flattened
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

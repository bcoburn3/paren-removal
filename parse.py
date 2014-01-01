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
                    sublst = tokens[(i + 1):(endidx + 2)]
                    res.append(parselist(sublst))
                    print(sublst)
                    i += endidx + 1
                    break
        else:
            res.append(elem)
            i += 1
    return res

print(parsestring("1 + ( 2 + ( 3 + 4 ) )"))
#should print:
#['1', '+', ['2', '+', ['3', '+', '4']]]

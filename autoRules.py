import liaBackend as backend

## Example rules line
## description=Dunk -> Expenses:Food:Coffee

def parseRuleList(src, splitStr = "->", pairDelim= "="):
    ruleList = []
    ruleFile = open(src, "r")
    for line in ruleFile:
        ruleList.append(parseRuleLine(line, splitStr = splitStr, pairDelim = pairDelim))
    ruleFile.close()
    return(ruleList)

def parseRuleLine(line, splitStr = "->", pairDelim= "="):
    """Parses out data from line of rules file"""
    splitLine    = str.split(line, splitStr)
    splitLine[0] = str.split(splitLine[0], pairDelim)
    return(recursiveTrim(splitLine))


def recursiveTrim(nestedList):
    """Recursively trims whitespace from strings in a nested list"""
    returnList = []         ## I hate I have to do this with python
    for curr in nestedList:
        if(isinstance(curr, str)):
            returnList.append(curr.strip())
        elif(isinstance(curr, list)):
            returnList.append(recursiveTrim(curr))
    return(returnList)

def stringIn(term, string):
    """checks to see if the first string is in the second"""
    return(term.lower() in string.lower())

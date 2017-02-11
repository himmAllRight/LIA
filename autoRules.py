import liaBackend as backend

## Example rules line
## description=Dunk -> Expenses:Food:Coffee

def parseRuleLine(line, splitStr = "->", pairDelim= ":", delim= "|"):
    """Parses out data from line of rules file"""
    splitLine   = str.split(line, splitStr)
    matchPair   = str.split(splitLine[0], pairDelim)
    actionPairs = list(map(lambda x : str.split(x, ":"), str.split(splitLine[1], delim)))

def recursiveTrim(nestedList):
    """Recursively trims whitespace from strings in a nested list"""
    returnList = []         ## I hate I have to do this with python
    for curr in nestedList:
        if(isinstance(curr, str)):
            returnList.append(curr.strip())
        elif(isinstance(curr, list)):
            returnList.append(recursiveTrim(curr))
    return(returnList)

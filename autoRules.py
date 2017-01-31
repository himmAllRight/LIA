import liaBackend as backend


## Example rules line
## description:Dunk -> description:DUNKINDONUTS|amount:15.00

def parseRuleLine(line, splitStr = "->", pairDelim= ":", delim= "|"):
    """Parses out data from line of rules file"""
    splitLine   = str.split(line, splitStr)
    matchPair   = str.split(splitLine[0], pairDelim)
    actionPairs = list(map(lambda x : str.split(x, ":"), str.split(splitLine[1], delim)))

import sys
import os
import argparse
import datetime

## Lia backend-code
## There should be no 'print' or 'input' calls here.

## File handeling Code
def openOutputFile(src, overwrite = False):
    """Handles opening the output file correctly"""
    if overwrite:
        return(open(src, "w"))
    else:
        return(open(src, "a"))

## Cache Queue Functions
def cacheInput(inputFile, cacheFileSRC, dateFormat, prepend = False, openMethod= "a"):
    """Goes through input file and caches it to be processed"""
    cacheFile = open(cacheFileSRC, openMethod)
    inputData = parseInput(inputFile, dateFormat)
    if prepend:
        prependToCache(inputData, cacheFile)
    else:
        appendToCache(inputData, cacheFile)
    cacheFile.close()

def parseInput(inputFile, dateFormat):
    """Reads an input file and converts it to the cache format"""
    header   = False
    inputData = []
    
    for line in inputFile:
        if (header == False):
            header = parseHeader(line)
        else:
            inputData.append(cleanLineData(parseLine(line, header), dateFormat))
    return(inputData)

## TODO
def prependToCache(inputFile, dateFormat):
    """Prepends the new input file to the cache to be processed first"""

def appendToCache(inputData, cacheFile, order=["date", "description", "amount"]):
    """Appends the Cache format input data to the cache-queue"""
    for item in inputData:
        cacheLine = lineDataToCacheLine(item, order = order)
        cacheFile.write(cacheLine + "\n")

def lineDataToCacheLine(lineData, order=["date", "description", "amount"], delim=","):
    """Converts a lineData item to a string to write to the cache"""
    lineDataList = []
    for dataName in order:
        lineDataList.append(lineData[dataName])
    return(delim.join(lineDataList))

def loadCache(cacheFileSRC, order=["date", "description", "amount"], delim=",", dateFormat="%Y/%m/%d"):
    """Loops through a cache file and parses/loads the data to a queue"""
    cacheFile = open(cacheFileSRC, "r")
    queueData = []
    for line in cacheFile:
        lineData = parseLine(line, order, delim)
        queueData.append(cleanLineData(lineData, dateFormat))
    cacheFile.close()
    return(queueData)

def writeWorkingCacheToFile(inputData, cacheFileSRC):
    cacheFile = open(cacheFileSRC, "w")
    appendToCache(inputData, cacheFile)
    cacheFile.close()
    

## Parser Code
def parseHeader(lineStr, delim = ","):
    """Parses the first line (header) to determine data order"""
    ## Split header into vector
    return(lineStr.split(delim))

def parseLine(line, lineOrder, delim = ","):
    """Parses out the information from a line """
    splitLine = line.split(delim)
    lineData = {"date"        : "",
                "amount"      : "",
                "description" : ""}

    for i in range(0, len(lineOrder)):
        headerItem = lineOrder[i]
        lineItem   = splitLine[i]

        if headerItem in lineData:
            lineData[headerItem] = lineItem

    return(lineData)

def cleanLineData(lineData, dateFormat, outputDateFormat = "%Y/%m/%d"):
    """Cleans the data of a line (format dates/clear extra whitespaces)"""
    # Clean Date to proper format
    d = datetime.datetime.strptime(lineData["date"], dateFormat)
    lineData["date"] = datetime.date.strftime(d, outputDateFormat)

    # Remove multiple spaces from description
    lineData["description"] = " ".join(lineData["description"].split())

    # Remove newlines
    for dataName in lineData:
        lineData[dataName] = lineData[dataName].rstrip("\n")

    return(lineData)

def entryInfo(lineData):
    """Returns a string of entry data"""
    return(lineData["date"] + " " + lineData["description"] + " " + lineData["amount"])

## Entry creation/modification functions
def modifyData(lineData, key, newValue):
    """Simply modifies the data of a lineData obj"""
    lineData[key] = newValue
    return(lineData)

def setMainAccount(lineData, mainAccount):
    """Sets user edited account name for the mainAccount value """
    lineData["mainAccount"] = mainAccount
    return(lineData)

def setSecondAccounts(lineData, secondaryAccounts):
    """Sets the secondary accounts data in lineData"""
    lineData["secondAccounts"] = secondaryAccounts

## Use this if more complicated method needed    
##    for (accountName, accountAmount) in secondaryAccounts:
##        lineData["secondAccounts"].append((accountName, accountAmount))
        
    return(lineData)
        

## Output Functions
def writeLedgerStatement(lineData, outFile):
    nameLine        = lineData["date"] + " " + lineData["description"] + "\n"
    mainAccountLine = "\t" + lineData["mainAccount"] + "\t" + lineData["amount"] + "\n"
    ## add loop here
    lastLines  = ""
    for line in lineData["secondAccounts"]:
        lastLines = lastLines + "\t" + line[0] + "\t" + line[1] + "\n"

    outFile.write(nameLine + mainAccountLine + lastLines + "\n")
    


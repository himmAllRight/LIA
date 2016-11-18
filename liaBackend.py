import sys
import os
import argparse
import datetime

## Lia backend-code

def parseHeader(lineStr, delim = ","):
    ## Split header into vector
    return(lineStr.split(delim))

def parseLine(line, lineOrder, delim = ","):
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
    # Clean Date to proper format
    d = datetime.datetime.strptime(lineData["date"], dateFormat)
    lineData["date"] = datetime.date.strftime(d, outputDateFormat)

    # Remove multiple spaces from description
    lineData["description"] = " ".join(lineData["description"].split())

    return(lineData)

def modifyLineData(lineData):
    newEntryInfo = lineData["date"] + " " + lineData["description"] + " " + lineData["amount"]
    print("\nAdding new entry: ", newEntryInfo)

    editList = ["description", "date", "amount"]

    for dataType in editList:
        editPrompt = dataType.capitalize() + " [" + lineData[dataType] + "]: "
        newInput = input(editPrompt)
        if(newInput != ""):
            lineData[dataType] = newInput
    return(lineData)

def setAccounts(lineData, importAccount = ""):
    ## Set main account
    editPrompt    = "Main account  [" + importAccount + "]: "
    editImportAccount = input(editPrompt)
    if(editImportAccount == ""):
        editImportAccount = importAccount
    lineData["mainAccount"] = editImportAccount

    ## Set movement account -- NOTE -- will eventually be a loop for multiple
    lineData = getSecondaryAccounts(lineData)

    return(lineData)

def getSecondaryAccounts(lineData):
    amount = lineData["amount"]
    lineData["secondAccounts"] = []
    accountAdd = True

    while(accountAdd != ""):
        accountAdd    = input("Secondary account(s): ")
        if(accountAdd != ""):
            amountPrompt  = "'" + accountAdd + "'"  + " amount: "
            accountAmount = input(amountPrompt)
            lineData["secondAccounts"].append((accountAdd, accountAmount))
        else:
            return(lineData)
        

def writeLedgerStatement(lineData, outFile):
    nameLine        = lineData["date"] + " " + lineData["description"] + "\n"
    mainAccountLine = "\t" + lineData["mainAccount"] + "\t" + lineData["amount"] + "\n"
    ## add loop here
    lastLines  = ""
    for line in lineData["secondAccounts"]:
        lastLines = lastLines + "\t" + line[0] + "\t" + line[1] + "\n"

    outFile.write(nameLine + mainAccountLine + lastLines + "\n")
    

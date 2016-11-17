import sys
import os
import argparse
import datetime

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
    

def main():
    """ The Main Class"""
    parser = argparse.ArgumentParser(description="Convert csv files to Ledger")
    parser.add_argument('-f','--input', help="Input csv file name", required=True)
    parser.add_argument('-o','--output', help="output ledger file name", required=True)
    parser.add_argument('-a','--import-account', help="Default import account", required=True)
    parser.add_argument('-d','--date-format', help="date-format", required=False)

    args = vars(parser.parse_args())

    inputFile     = open(args['input'], "r")
    outputFile    = open(args['output'], "w")
    importAccount = args['import_account']
    dateFormat    = "%m/%d/%Y"
    
    if args['date_format']:
        dateformat = args['date_format']

    header = False
    for line in inputFile:
        if(header == False):
            header = parseHeader(line)
        else:
            lineData = parseLine(line, header)
            lineData = cleanLineData(lineData, dateFormat)
            lineData = modifyLineData(lineData)
            lineData = setAccounts(lineData, importAccount = importAccount)
            writeLedgerStatement(lineData, outputFile)

    inputFile.close()
    outputFile.close()
    print("All done! Have a great day!")
        

class __main__:
    main()


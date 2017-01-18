#import sys
import os
import argparse
#import datetime
import liaBackend as backend

## All the CLI Code
def getUserInput(promptStr, defaultValue = False):
    """Gets the input from use. Returns False if no input"""
    response = input(promptStr)
    if(response == ""):
        return(defaultValue)
    else:
        return(response)

def modifyLinePrompt(lineData, editList= ["description", "date", "amount"]):
    """Loops through and prompts user of any data modifications to line"""
    print("\nAdding new entry: " + backend.entryInfo(lineData))
    
    for dataType in editList:
        editPrompt = dataType.capitalize() + " [" + lineData[dataType] + "]: "
        response = getUserInput(editPrompt)
        if(response):
            backend.modifyData(lineData, dataType, response)
    return(lineData)

def setAccountsPrompt(lineData, importAccount = ""):
    """Calls the prompts to set the accounts (will also check rules when added)"""

    ## In the future, here is where the rules will be checked/called to see if
    ## there is anything to pass as a secondary account's default name.
    
    ## For now, just enjoy the nested return call :P
    lineData = mainAccountPrompt(lineData, importAccount = importAccount)
    lineData = secondAccountsPrompt(lineData)
    return(lineData)

def mainAccountPrompt(lineData, importAccount = ""):
    """Prompts the user for information to set the main account"""
    editPrompt = "Main account [" + importAccount + "]: "
    editImportAccount = getUserInput(editPrompt, defaultValue = importAccount)

    return(backend.setMainAccount(lineData, editImportAccount))

    

def secondAccountsPrompt(lineData):
    """Prompts the user for the secondary account(s) information"""
    secondAccounts = []
    accountAdd = True

    while(accountAdd or secondAccounts == []):
        if(not(accountAdd) and secondAccounts == []):
            print("At least one secondary account must be specified. Try again.")
        accountAdd = getUserInput("Secondary account(s): ", defaultValue = False)
        if(accountAdd):
            accountAmount = getUserInput("'" + accountAdd + "'" + " amount: ", defaultValue = "")
            secondAccounts.append((accountAdd, accountAmount))
    return(backend.setSecondAccounts(lineData, secondAccounts))
        
    
    

## Main CLI Loop
def main():
    """ The Main Class"""
    parser = argparse.ArgumentParser(description="Convert csv files to Ledger")
    parser.add_argument('-f','--input', help="Input csv file name", required=True)
    parser.add_argument('-o','--output', help="output ledger file name", required=True)
    parser.add_argument('-a','--import-account', help="Default import account", required=True)
    parser.add_argument('-d','--date-format', help="date-format", required=False)
    parser.add_argument('-r', '--overwrite', help="Overwrite output file. Defaults to append", required=False)

    args = vars(parser.parse_args())

    inputFile     = open(args['input'], "r")
    outputFile    = backend.openOutputFile(args['output'], args['overwrite'])
    cacheFileSRC  = "./cache.csv"
    importAccount = args['import_account']
    dateFormat    = "%m/%d/%Y"
    
    if args['date_format']:
        dateformat = args['date_format']

    backend.cacheInput(inputFile, cacheFileSRC, dateFormat)
    queueData = backend.loadCache(cacheFileSRC)

    skipProcess = input("skip Process? (For Testing)")
    
    import atexit
    atexit.register(backend.writeWorkingCacheToFile, queueData, cacheFileSRC)
    
    if(skipProcess == "n"):
        for lineData in queueData:
            lineData = modifyLinePrompt(lineData)
            lineData = setAccountsPrompt(lineData, importAccount = importAccount)
            backend.writeLedgerStatement(lineData, outputFile)
            ## If loop through all, delete cache file
            os.remove(cacheFileSRC)

    inputFile.close()
    outputFile.close()
    print("All done! Have a great day!")
        

class __main__:
    main()


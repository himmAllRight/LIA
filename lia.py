#import sys
import os
import argparse
import readline
import liaBackend as backend
import autoRules as rules

## All the CLI Code
def rlinput(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return input(prompt)
   finally:
      readline.set_startup_hook()

def getUserInput(promptStr, prefill= '', defaultValue = False, force= False):
   """Gets the input from use. Returns False if no input"""
   response = rlinput(promptStr, prefill= prefill)
   if(force):
      while(response == ""):
         print("Sorry, a value must be provided for this. Please try again.")
         response = rlinput(promptStr, prefill= prefill)
      return(response)
   else:
      if(response == ""):
         return(defaultValue)
      else:
         return(response)

def modifyLinePrompt(lineData, editList= ["description", "date", "amount"]):
    """Loops through and prompts user of any data modifications to line"""
    print("\nAdding new entry: " + backend.entryInfo(lineData))
    
    for dataType in editList:
        editPrompt = dataType.capitalize() + ": "
        response = getUserInput(editPrompt, prefill= lineData[dataType])
        if(response):
            backend.modifyData(lineData, dataType, response)
    return(lineData)

def setAccountsPrompt(lineData, ruleList= False, importAccount = ""):
    """Calls the prompts to set the accounts (will also check rules when added)"""

    ## In the future, here is where the rules will be checked/called to see if
    ## there is anything to pass as a secondary account's default name.
    
    ## For now, just enjoy the nested return call :P
    lineData = mainAccountPrompt(lineData, importAccount = importAccount)
    lineData = secondAccountsPrompt(lineData, ruleList = ruleList)
    return(lineData)

def mainAccountPrompt(lineData, importAccount = ""):
    """Prompts the user for information to set the main account"""
    editPrompt = "Main account: "
    editImportAccount = getUserInput(editPrompt, prefill= importAccount, defaultValue = importAccount, force= True)

    return(backend.setMainAccount(lineData, editImportAccount))

    
def secondAccountsPrompt(lineData, ruleList=False):
   """Prompts the user for the secondary account(s) information"""
   secondAccounts = []
   accountAdd = True
   if(ruleList):
      prefill = rules.matchRuleData(lineData, ruleList)
   else:
      prefill = ""

   while(accountAdd or secondAccounts == []):
      if(not(accountAdd) and secondAccounts == []):
         print("At least one secondary account must be specified. Try again.")
      accountAdd = getUserInput("Secondary account(s): ", prefill = prefill)
      if(accountAdd):
         prefill = ""
         accountAmount = getUserInput("'" + accountAdd + "'" + " amount: ", defaultValue = "")
         secondAccounts.append((accountAdd, accountAmount))
   return(backend.setSecondAccounts(lineData, secondAccounts))

def cacheProcess(queueData,ruleList, importAccount, outputFile, cacheFileSRC):
    """CLI for processing input files or cached items"""
    for i in range(0,len(queueData)):
        lineData = modifyLinePrompt(queueData[0])
        lineData = setAccountsPrompt(lineData, ruleList = ruleList, importAccount = importAccount)
        backend.writeLedgerStatement(lineData, outputFile)
        queueData.pop(0)
        ## If loop through all, delete cache file
    os.remove(cacheFileSRC)

def manualAddProcess(importAccount, outputFile, dateFormat, ruleList= False, orderList= ["description", "date", "amount"]):
    """CLI sequence for manually adding entries"""
    head, *tail = orderList
    userInput = getUserInput("Enter in transaction " +  head + ": ")
    lineData = {}
    while userInput:
        lineData["mainAccount"] = importAccount
        lineData[head] = userInput
        for inputType in tail:
            lineData[inputType] = getUserInput("Enter in " + inputType + ": ", force=True)
        lineData = backend.cleanLineData(lineData, dateFormat)
        lineData = secondAccountsPrompt(lineData, ruleList = ruleList)
        backend.writeLedgerStatement(lineData, outputFile)
        print("'" + lineData[head] + "'" + " added to ledger journal.\n")
        
        userInput = getUserInput("Enter in transaction " +  head + ": ")
        
    

## Main CLI Loop
def main():
    """ The Main Class"""
    parser = argparse.ArgumentParser(description="Convert csv files to Ledger")
    parser.add_argument('-f','--input', help="Input csv file name", required=False)
    parser.add_argument('-r','--rules', help="Automatic rules file", required=False)
    parser.add_argument('-m','--manual',action = 'store_true', help="Manually write new Transactions instead of file import.",
                        required=False)
    parser.add_argument('-o','--output', help="output ledger file name", required=True)
    parser.add_argument('-a','--import-account', help="Default import account", required=True)
    parser.add_argument('-d','--date-format', help="date-format", required=False)
    parser.add_argument('-w', '--overwrite', help="Overwrite output file. Defaults to append", required=False)

    args = vars(parser.parse_args())

    
    if(args['input']):
        inputFile     = open(args['input'], "r")
    else:
        inputFile = False

    if(args['rules']):
       ruleList = rules.parseRuleList(args['rules'])
    else:
       ruleList = False

    manualInput   = args['manual']
    outputFile    = backend.openOutputFile(args['output'], args['overwrite'])
    cacheFileSRC  = "./cache.csv"
    importAccount = args['import_account']
    dateFormat    = "%m/%d/%Y"
    
    if args['date_format']:
        dateFormat = args['date_format']

    ## Load Cache
    if(inputFile):
        backend.cacheInput(inputFile, cacheFileSRC, dateFormat)
    queueData = backend.loadCache(cacheFileSRC)

    ## Escape Case
    import atexit
    atexit.register(backend.writeWorkingCacheToFile, queueData, cacheFileSRC)

    ## Manual or Import process
    if(manualInput):
        manualAddProcess(importAccount, outputFile, dateFormat, ruleList= ruleList)
    else:
        cacheProcess(queueData, ruleList, importAccount, outputFile, cacheFileSRC)
        
    ## Close out and wrapup
    if(not(manualInput)):
        inputFile.close()
    outputFile.close()
    print("All done! Have a great day!")
        

class __main__:
    main()


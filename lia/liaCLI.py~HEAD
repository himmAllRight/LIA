#import sys
import argparse
import os
import readline


import lia.liaBackend as backend
import lia.autoRules as rules

## All the CLI Code
def rlinput(prompt, prefill='', promptColor = False):
   if(promptColor):
      colorTags = ['\x1b[0;32m', '\033[1;m']
   else:
      colorTags = ['','']
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return input(colorTags[0] + prompt + colorTags[1])
   finally:
      readline.set_startup_hook()

def getUserInput(promptStr, prefill= '', defaultValue = False, force= False, promptColor=False):
   """Gets the input from use. Returns False if no input"""
   response = rlinput(promptStr, prefill= prefill, promptColor=promptColor)
   if(force):
      while(response == ""):
         print("Sorry, a value must be provided for this. Please try again.")
         response = rlinput(promptStr, prefill= prefill, promptColor= promptColor)
      return(response)
   else:
      if(response == ""):
         return(defaultValue)
      else:
         return(response)

def modifyLinePrompt(lineData, editList= ["description", "date", "amount"], promptColor=False):
    """Loops through and prompts user of any data modifications to line"""
    print("\nAdding new entry: " + backend.entryInfo(lineData))
    
    for dataType in editList:
        editPrompt = dataType.capitalize() + ": "
        response = getUserInput(editPrompt, prefill= lineData[dataType], promptColor= promptColor)
        if(response):
            backend.modifyData(lineData, dataType, response)
    return(lineData)

def setAccountsPrompt(lineData, ruleList= False, importAccount = "", promptColor = False):
    """Calls the prompts to set the accounts (will also check rules when added)"""

    ## In the future, here is where the rules will be checked/called to see if
    ## there is anything to pass as a secondary account's default name.
    
    ## For now, just enjoy the nested return call :P
    lineData = mainAccountPrompt(lineData, importAccount = importAccount, promptColor= promptColor)
    lineData = secondAccountsPrompt(lineData, ruleList = ruleList, promptColor= promptColor)
    return(lineData)

def mainAccountPrompt(lineData, importAccount = "", promptColor=False):
    """Prompts the user for information to set the main account"""
    editPrompt = "Main account: "
    editImportAccount = getUserInput(editPrompt, prefill= importAccount, defaultValue = importAccount, force= True, promptColor= promptColor)

    return(backend.setMainAccount(lineData, editImportAccount))

    
def secondAccountsPrompt(lineData, ruleList=False, promptColor=False):
   """Prompts the user for the secondary account(s) information"""
   secondAccounts = []

   if(ruleList):
      prefill = rules.matchRuleData(lineData, ruleList)
   else:
      prefill = ""

   force = True
   accountAmount = True  ## Ugh this is such a hack...
   while(accountAmount != ""):
      accountAmount = ""
      accountAdd    = getUserInput("Secondary account(s): ", prefill = prefill, defaultValue = "", force= force, promptColor= promptColor)
      if(accountAdd != ""):
         accountAmount = getUserInput("'" + accountAdd + "'" + " amount: ", defaultValue = "", promptColor= promptColor)
         secondAccounts.append((accountAdd, accountAmount))
         force = False
   return(backend.setSecondAccounts(lineData, secondAccounts))



def cacheProcess(queueData,ruleList, importAccount, outputFile, cacheFileSRC, promptColor= False):
    """CLI for processing input files or cached items"""
    for i in range(0,len(queueData)):
        lineData = modifyLinePrompt(queueData[0], promptColor= promptColor)
        lineData = setAccountsPrompt(lineData, ruleList = ruleList, importAccount = importAccount, promptColor= promptColor)
        backend.writeLedgerStatement(lineData, outputFile)
        queueData.pop(0)
        ## If loop through all, delete cache file
    os.remove(cacheFileSRC)

def manualAddProcess(importAccount, outputFile, dateFormat, ruleList= False, orderList= ["description", "date", "amount"], promptColor= False):
    """CLI sequence for manually adding entries"""
    head, tail = orderList[0], orderList[1:]
    userInput = getUserInput("Enter in transaction " +  head + ": ", promptColor= promptColor)
    lineData = {}
    while userInput:
        lineData["mainAccount"] = importAccount
        lineData[head] = userInput
        for inputType in tail:
            lineData[inputType] = getUserInput("Enter in " + inputType + ": ", force=True, promptColor= promptColor)
        lineData = backend.cleanLineData(lineData, dateFormat)
        lineData = secondAccountsPrompt(lineData, ruleList = ruleList)
        backend.writeLedgerStatement(lineData, outputFile)
        print("'" + lineData[head] + "'" + " added to ledger journal.\n")
        
        userInput = getUserInput("Enter in transaction " +  head + ": ", promptColor= promptColor)



import os
import sys
import functools
import liaBackend as backend

def test_parseHeader():
    testString = ",,,date,,amount,,description,"
    testOutput = backend.parseHeader(testString)
    expectedOutput = ['', '', '', 'date', '', 'amount', '', 'description', '']
    return(testOutput == expectedOutput)
    
def test_parseLine():
    header   = backend.parseHeader(",,date,amount,description,,")
    lineData = backend.parseLine(",,09/06/1991,75.19,line statement,,", header)
    expected =  {'description': 'line statement'
                , 'date': '09/06/1991'
                , 'amount': '75.19'}
    return(lineData == expected)

def test_cleanLineData():
    lineData    = {'description': 'line statement          '
                   , 'date': '09/06/1991'
                   , 'amount': '75.19'}
    dateFormat  = "%m/%d/%Y"
    cleanedLine = backend.cleanLineData(lineData, dateFormat)
    expected    = {'description': 'line statement'
                   , 'date': '1991/09/06'
                   , 'amount': '75.19'}

    return(cleanedLine == expected)

def test_entryInfo():
    lineData    = {'description': 'line statement          '
                   , 'date': '09/06/1991'
                   , 'amount': '75.19'}
    resultLine  = backend.entryInfo(lineData)
    expected    = '09/06/1991 line statement           75.19'
    return(resultLine == expected)

def test_modifyData():
    startLineData     = {'description': 'line statement          '
                         , 'date': '09/06/1991'
                         , 'amount': '75.19'}
    newLineData       = backend.modifyData(startLineData, "date", '10/14/1991')
    expectedLinedData = {'description': 'line statement          '
                         , 'date': '10/14/1991'
                         , 'amount': '75.19'}
    return(newLineData == expectedLinedData)

### These tests require some refactoring to isolate IO
### I am going to see if I can factor out some common IO
### tasks into a few very basic IO functions, and then have
### the logic of these functions be pure and testable.

## test_setAccounts()
## test_getSecondaryAccounts()


# Just until I write real ones
def testTrue():
    return(True)

# Execute Tests
testList =  [["True", testTrue()]
             ,["parseHeader", test_parseHeader()]
             ,["parseLine", test_parseLine()]
             ,["cleanLineData", test_cleanLineData()]
             ,["entryInfo", test_entryInfo()]
             ,["modifyData", test_modifyData()]]
failedTests = []

largestTestName =  functools.reduce(max, map(lambda x: len(x[0]), testList))


for test in testList:
    print(test[0].rjust(largestTestName), "Test: ", test[1])
    if(test[1] == False):
        failedTests.append(test[0])

## Break if 1 or more tests failed    
if(len(failedTests) > 0):
    failureMessage = "One or more tests failed! [" + ", ".join(failedTests) + "]"
    sys.exit(failureMessage)

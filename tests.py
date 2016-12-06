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
                , 'date': '09/06/1992'
                , 'amount': '75.19'}
    return(lineData == expected)


# Just until I write real ones
def testTrue():
    return(True)

# Execute Tests
testList =  [["True", testTrue()]
             ,["parseHeader", test_parseHeader()]
             ,["parseLine", test_parseLine()]]

largestTestName =  functools.reduce(max, map(lambda x: len(x[0]), testList))

for test in testList:
    print(test[0].rjust(largestTestName), "Test: ", test[1])


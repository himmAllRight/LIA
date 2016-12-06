import os
import sys
import functools
import liaBackend as backend

def test_parseHeader():
    testString = ",,,date,,amount,,description,"
    testOutput = backend.parseHeader(testString)
    expectedOutput = ['', '', '', 'date', '', 'amount', '', 'description', '']
    return(testOutput == expectedOutput)
    

# Just until I write real ones
def testTrue():
    return(True)

# Execute Tests
testList =  [["True", testTrue()]
            ,["parseHeader", test_parseHeader()]]

largestTestName =  functools.reduce(max, map(lambda x: len(x[0]), testList))

for test in testList:
    print(test[0].rjust(largestTestName), "Test: ", test[1])


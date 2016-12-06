import os
import sys
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

print(testTrue())
print(test_parseHeader())


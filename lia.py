#import sys
#import os
import argparse
#import datetime
import liaBackend as backend

## All the CLI Code


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
            header = backend.parseHeader(line)
        else:
            lineData = backend.parseLine(line, header)
            lineData = backend.cleanLineData(lineData, dateFormat)
            lineData = backend.modifyLineData(lineData)
            lineData = backend.setAccounts(lineData, importAccount = importAccount)
            backend.writeLedgerStatement(lineData, outputFile)

    inputFile.close()
    outputFile.close()
    print("All done! Have a great day!")
        

class __main__:
    main()


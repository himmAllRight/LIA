import argparse
import os
import readline

import lia as ui
import liaBackend as backend
import autoRules as rules


def argSet(key, args, fn, failReturn= False):
   if(args[key]):
      return(fn(key, args[key]))
   else:
      return(failReturn)


## Main CLI Loop
def main():
    """ The Main Class"""
    parser = argparse.ArgumentParser(description="Convert csv files to Ledger")
    parser.add_argument('-f', '--input', help="Input csv file name", required=False)
    parser.add_argument('-r', '--rules', help="Automatic rules file", required=False)
    parser.add_argument('-m', '--manual', action='store_true',
                        help="Manually write new Transactions instead of file import.",
                        required=False)
    parser.add_argument('-o', '--output', help="output ledger file name", required=True)
    parser.add_argument('-c', '--color', action="store_true", help="Turns on the colored output", required=False)
    parser.add_argument('-a', '--import-account', help="Default import account", required=True)
    parser.add_argument('-d', '--date-format', help="date-format", required=False)
    parser.add_argument('-w', '--overwrite', help="Overwrite output file. Defaults to append", required=False)

    args = vars(parser.parse_args())

    promptColor = False

    inputFile = argSet('input', args, lambda key, value: open(value, "r"))
    ruleList = argSet('rules', args, lambda key, value: rules.parseRuleList(value))
    promptColor = argSet('color', args, lambda key, value: True)

    # if(args['input']):
    #     inputFile     = open(args['input'], "r")
    # else:
    #     inputFile = False
    # if(args['rules']):
    #    ruleList = rules.parseRuleList(args['rules'])
    # else:
    #    ruleList = False


    manualInput = args['manual']
    outputFile = backend.openOutputFile(args['output'], args['overwrite'])
    cacheFileSRC = "./cache.csv"
    importAccount = args['import_account']
    dateFormat = "%m/%d/%Y"

    if args['date_format']:
        dateFormat = args['date_format']

    ## Load Cache
    if (inputFile):
        backend.cacheInput(inputFile, cacheFileSRC, dateFormat)
    queueData = backend.loadCache(cacheFileSRC)

    ## Escape Case
    import atexit
    atexit.register(backend.writeWorkingCacheToFile, queueData, cacheFileSRC)

    ## Manual or Import process
    if (manualInput):
        ui.manualAddProcess(importAccount, outputFile, dateFormat, ruleList=ruleList, promptColor=promptColor)
    else:
        ui.cacheProcess(queueData, ruleList, importAccount, outputFile, cacheFileSRC, promptColor=promptColor)

    ## Close out and wrapup
    if (not (manualInput)):
        inputFile.close()
    outputFile.close()
    print("All done! Have a great day!")


class __main__:
    main()


if __name__ == "__main__":
    # execute only if run as a script
    main()
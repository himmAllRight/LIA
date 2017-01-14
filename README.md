# LIA (Ledger Import Assistant)

[![Build Status](https://travis-ci.org/himmAllRight/LIA.svg?branch=master)](https://travis-ci.org/himmAllRight/LIA/)

LIA is a simple command-line python application that can help import exported Cedit Card and Bank statement csv files into a ledger journal. There are many other great convert/import options out there. However, I found their setup to often be a bit more complicated than what I needed initially, so I decided to write my own tool. Development of LIA will expand with my use of ledger.

### Features:
- CSV files are read in and converted to simple ledger journal statements.
- Data order is recognized by a header mechanism
- Prompts the user to potentially edit the transaction data (defaults to csv value)
- Supports multiple destination accounts

- NOTE: I think the output file may be overwritten right now

### Command Line Options
| Flags | description |
|-------|-------------|
| -f, --import | input csv file to convert |
| -o, --output | Output ledger file name |
| -r, --overwrite | Overwrites the output file. Appends by default |
| -a, --import-account | The account the import data is from |
| -d, --date-format | the date format for dates in the csv (ex: "%m/%d/%Y") |
| -h | Help |


### Instructions

_To add later_

### Example
`python3 lia.py -f credit-card.csv -o ledger.dat -a "Liabilities:CreditCard:Discover" -d "%m/%d/%Y"`

### Future TODO Features
- [X] Output appends, unless --overwrite flag
- [ ] Option to have statements with reconciled indicator
- [ ] When looping through an input file, it copies the input file to a temp and pops items off as it works through them. This way, if you stop part-way through, you can pick up where it was last left off.
- [ ] When user edits data, default values are editable in the prompt
- [ ] User can setup rules/parsers to default transaction placement. (ex: anything from "cumberland farms" will default to Expenses:Transportation:Gas)



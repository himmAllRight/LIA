LIA="lia/lia.py"
INPUT1="test-files/test-input-small.csv"
INPUT2="test-files/test-numbered-input.csv"
OUTPUT="test-files/test-output.dat"
RULES="test-files/rules-test.txt"

ACCOUNT="Liabilities:CreditCard:Ryan"


run:
	python3 $(LIA) -f $(INPUT1) -o $(OUTPUT) -a $(ACCOUNT) -r $(RULES) -c
run2:
	python3 $(LIA) -f $(INPUT2) -o $(OUTPUT) -a $(ACCOUNT) -r $(RULES) -c
manual:
	python3 $(LIA) -m -o $(OUTPUT) -a $(ACCOUNT) -r $(RULES) -c
cacheRun:
	python3 $(LIA) -o $(OUTPUT) -a $(ACCOUNT) -r $(RULES) -c
build:
	nuitka --recurse-all $(LIA)

clean:
	rm -rf lia.build lia.exe cache.csv $(OUTPUT)

test:
	python3 tests.py
test2:
	python tests.py

all:
	make clean build test run

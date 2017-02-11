run:
	python3 lia.py -f test-files/test-input-small.csv -o test-files/test-output.dat -a "Liabilities:CreditCard:Ryan" -r "test-files/rules-test.txt"
run2:
	python3 lia.py -f test-files/test-numbered-input.csv -o test-files/test-output.dat -a "Liabilities:CreditCard:Ryan" -r "test-files/rules-test.txt"
manual:
	python3 lia.py -m -o test-files/test-output.dat -a "Liabilities:CreditCard:Ryan" -r "test-files/rules-test.txt"
cacheRun:
	python3 lia.py -o test-files/test-output.dat -a "Liabilities:CreditCard:Ryan"
build:
	nuitka --recurse-all lia.py

clean:
	rm -rf lia.build lia.exe test-files/test-output.dat cache.csv

test:
	python3 tests.py

all:
	make clean build test run

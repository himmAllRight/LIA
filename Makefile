run:
	python3 lia.py -f test-files/test-input-small.csv -o test-files/test-output.dat -a "Liabilities:CreditCard:Ryan"
build:
	nuitka --recurse-all lia.py

clean:
	rm -rf lia.build lia.exe test-files/test-output.dat

test:
	python3 tests.py

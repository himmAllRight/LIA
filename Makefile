build:
	nuitka --recurse-all lia.py

clean:
	rm -rf lia.build lia.exe

test:
	python3 tests/tests.py

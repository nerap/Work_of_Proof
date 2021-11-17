# define the name of the virtual environment directory
VENV := venv

# default target, when make executed without arguments
all: venv

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip3 install -r requirements.txt

# venv is a shortcut target
venv: $(VENV)/bin/activate

run: venv
	./$(VENV)/bin/python3 main.py

req:
	$(VENV)/bin/pip3 freeze > requirements.txt
	git add requirements.txt

hook:
	git config core.hooksPath .githooks

#Running test
test: venv
	rm -rf test/wallet_test/test_*
	./$(VENV)/bin/python3 -m unittest test/*_test.py
	rm -rf test/wallet_test/test_*

re : clean all

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

.PHONY: all venv run clean re hook req
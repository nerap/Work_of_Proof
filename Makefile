# define the name of the virtual environment directory
VENV := venv

# default target, when make executed without arguments
all: venv

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt

# venv is a shortcut target
venv: $(VENV)/bin/activate

run: venv
	./$(VENV)/bin/python3 pytest.py

m_one:
	./venv/bin/python3 main.py --port=8000 --mine=1

m_two:
	./venv/bin/python3 main.py --port=8001 --mine=1

m_three:
	./venv/bin/python3 main.py --port=8002 --mine=1

re : clean all

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

.PHONY: all venv run clean re
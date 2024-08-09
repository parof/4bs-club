# Define variables. Set to the python and pip executables you want to use.
PYTHON = python3
PIP = pip3
REQUIREMENTS = requirements.txt

# Default target.
all: run

# Target to run the main script.
run:
	$(PYTHON) main.py

# Target to install dependencies.
dependencies:
	$(PIP) install -r $(REQUIREMENTS)

# Clean target to remove installed packages (optional).
clean:
	$(PIP) uninstall -r $(REQUIREMENTS) -y

.PHONY: all run dependencies clean

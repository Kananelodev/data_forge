VENV=.venv
ifeq ($(OS),Windows_NT)
BIN=$(VENV)/Scripts
else
BIN=$(VENV)/bin
endif
PY=$(BIN)/python

.PHONY: setup play gates quest

setup:            ## create venv + install deps
	python -m venv $(VENV)
	$(PY) -m pip install -q --upgrade pip
	$(PY) -m pip install -q -r requirements.txt
	@echo "Forge ready. Run 'make play'."

play:             ## take a turn: strike gates, update board + map (same as a push)
	$(PY) -m forge.update

gates:            ## just run the gate tests, verbose
	$(PY) -m pytest gates -v

quest:            ## start a journal entry: make quest Q=q01
	@test -n "$(Q)" || (echo "usage: make quest Q=q01" && exit 1)
	@test ! -f journal/$(Q).md || (echo "journal/$(Q).md already exists" && exit 1)
	@sed -e "s/qXX/$(Q)/g" -e "s/YYYY-MM-DD/$$(date +%F)/" journal/TEMPLATE.md > journal/$(Q).md
	@echo "Created journal/$(Q).md — write it in your own words."

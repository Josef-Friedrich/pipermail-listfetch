install:
	virtualenv /opt/pyenvs/pipermail_listfetch
	poetry env use /opt/pyenvs/pipermail_listfetch/bin/python
	poetry install

run: pipermail-listfetch.py

.PHONY: install run

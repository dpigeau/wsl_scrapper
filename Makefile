init:
	pip install -r requirements.txt

debug:
	python wsl_scrapper/debug.py

scrap:
	python wsl_scrapper/scrap.py

.PHONY: tests
tests:
	rm -rf data/tests/
	pytest tests/.

load-dev:
	python scrapper/load.py dev
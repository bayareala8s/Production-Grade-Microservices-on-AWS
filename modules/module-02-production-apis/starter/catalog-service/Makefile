.PHONY: install test run export-openapi

install:
\tpython -m pip install -r requirements.txt -r requirements-dev.txt

test:
\tpytest -q

run:
\tuvicorn app.main:app --reload --port 8000

export-openapi:
\tpython scripts/export_openapi.py --base-url http://localhost:8000 --out openapi.generated.json



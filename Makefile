.PHONY: up down test demo lint aws-start aws-stop aws-deploy aws-destroy verify-labs verify-all diagrams labs-start labs-stop labs-status labs-restart

diagrams:
	chmod +x scripts/export-diagrams.sh scripts/export-aws-drawio.sh
	./scripts/export-diagrams.sh
	@if [ -x .venv-diagrams/bin/python ]; then \
		.venv-diagrams/bin/python scripts/generate-aws-stencil-diagrams.py; \
		.venv-diagrams/bin/python scripts/generate-aws-drawio-sources.py; \
	else \
		echo "Tip: python3 -m venv .venv-diagrams && .venv-diagrams/bin/pip install -r scripts/requirements-diagrams.txt"; \
		python3 scripts/generate-aws-drawio-sources.py 2>/dev/null || true; \
	fi
	./scripts/export-aws-drawio.sh

up:
	docker compose up --build -d

down:
	docker compose down

test:
	./scripts/run-all-tests.sh

demo:
	chmod +x scripts/demo-platform.sh
	./scripts/demo-platform.sh

verify-labs:
	./scripts/verify-all-labs.sh

verify-aws-labs:
	./scripts/verify-aws-labs.sh

verify-all: test verify-labs

aws-start:
	./scripts/aws-start.sh

aws-stop:
	./scripts/aws-stop.sh

aws-deploy:
	./scripts/aws-deploy.sh

aws-destroy:
	./scripts/aws-destroy.sh

labs-start:
	chmod +x scripts/labs-start.sh scripts/labs-stop.sh scripts/labs-status.sh scripts/labs-restart.sh
	./scripts/labs-start.sh --all

labs-stop:
	chmod +x scripts/labs-start.sh scripts/labs-stop.sh scripts/labs-status.sh
	./scripts/labs-stop.sh

labs-status:
	chmod +x scripts/labs-status.sh
	./scripts/labs-status.sh

labs-restart:
	chmod +x scripts/labs-restart.sh
	./scripts/labs-restart.sh --all

logs:
	docker compose logs -f

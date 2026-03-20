.PHONY: benchmark api test

benchmark:
	python scripts/run_benchmark.py --config configs/demo_hybrid.yaml

api:
	uvicorn vehicle_bank.api:app --reload

test:
	pytest -q

# Target to run the main FastAPI app
main:
	@echo "Starting FastAPI main app..."
	.venv/bin/python -m uvicorn app.main:app --reload

# Target to run the first dummy server
dummy_a:
	@echo "Starting Service A..."
	.venv/bin/python tests/dummies/service_a.py

# Target to run the second dummy server
dummy_b:
	@echo "Starting Service B..."
	.venv/bin/python tests/dummies/service_b.py


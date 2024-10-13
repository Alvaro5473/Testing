PYTHON=python

run_app:
	$(PYTHON) app.py

test_unit:
	$(PYTHON) test_unit.py

test_integration:
	$(PYTHON) -m unittest test_app.py

test_functional:
	$(PYTHON) test_functional.py

test_security:
	pytest test_security.py

test_performance:
	locust -f locustfile.py

all: run_app test_unit test_integration test_functional test_security test_performance

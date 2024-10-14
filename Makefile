COVERAGE=coverage run

lint:
	pylint *.py

trivy:
	trivy fs .

run_app:
	$(COVERAGE) app.py

test_unit:
	$(COVERAGE) test_unit.py

test_integration:
	$(COVERAGE) -m unittest test_app.py

test_functional:
	$(COVERAGE) test_functional.py

test_security:
	$(COVERAGE) test_security.py

test_performance:
	$(COVERAGE) locustfile.py

all: lint run_app test_unit test_integration test_functional test_security test_performance trivy

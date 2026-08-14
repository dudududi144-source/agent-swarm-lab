.PHONY: test run status reset clean

test:
	python test.py

run:
	python run.py "$(IDEA)"

status:
	python run.py --status

reset:
	python run.py --reset

clean:
	rm -rf output/
	rm -f agents/notifications.log
	rm -f agents/metrics.json

install:
	pip install -r requirements.txt
HOST=192.168.0.23

rsync:
	rsync -rv --exclude '.idea' $$(pwd) pi@$(HOST):~/

start: stop-logger
	docker-compose up -d
	python temp-logger.py &

stop-logger:
	pkill -f temp-logger.py

start-dev:
	docker-compose -f docker-compose-python.yaml up  -d --build

influx:
	docker-compose exec influxdb influx

down-dev:
	docker-compose -f docker-compose-python.yaml down
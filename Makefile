HOST=raspberrypi.local

rsync:
	rsync -rv --exclude '.idea' --exclude '.git' --exclude '.env' --exclude 'git' $$(pwd) pi@$(HOST):~/

ssh:
	ssh pi@$(HOST)

start:
	docker-compose up -d --build

stop:
	docker-compose stop

influx:
	docker-compose exec influxdb influx

github-logger:
	screen -d -m python rpi-temp-sensor/temp-logger-to-gh.py
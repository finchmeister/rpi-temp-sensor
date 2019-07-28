HOST=192.168.0.23

rsync:
	rsync -rv --exclude '.idea' --exclude '.git' --exclude '.env' $$(pwd) pi@$(HOST):~/

start:
	docker-compose up -d --build

influx:
	docker-compose exec influxdb influx

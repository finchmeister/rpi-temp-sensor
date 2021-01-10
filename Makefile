HOST=192.168.1.147
HOST2=192.168.1.148

rsync:
	rsync -rv --exclude '.idea' --exclude '.git' --exclude '.env' --exclude 'git' --exclude 'checkpoint.txt' $$(pwd) pi@$(HOST2):~/

ssh:
	ssh pi@$(HOST)

start-db:
	docker-compose up -d --build

start-legacy:
	docker-compose -f docker-compose.yaml -f docker-compose-python-script.yaml up -d --build

stop:
	docker-compose stop

influx:
	docker-compose exec influxdb influx

update-monitor-lambda:
	cd temp-logger-monitor; zip ../my-deployment-package.zip monitor.py
	aws lambda update-function-code --function-name temp-sensor-monitor --zip-file fileb://my-deployment-package.zip | cat
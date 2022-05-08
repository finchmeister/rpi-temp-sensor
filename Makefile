HOST_PI_1=192.168.0.31
HOST_PI_2=192.168.0.30

rsync:
	rsync -rv --exclude '.idea' --exclude '.git' --exclude '.env' --exclude 'git' --exclude 'checkpoint.txt' $$(pwd) pi@$(HOST_PI_2):~/

deploy-temp-logger:
	rsync -rv --exclude '.idea' --exclude '.git' --exclude '.env' --exclude 'git' --exclude 'checkpoint.txt' $$(pwd) pi@$(HOST_PI_1):~/

ssh-pi-1:
	ssh pi@$(HOST_PI_1)

ssh-pi-2:
	ssh pi@$(HOST_PI_1)

# Run from the context of the PI
start-db:
	docker-compose up -d --build

# Run from the context of the PI
stop:
	docker-compose stop

# Run from the context of the PI
influx:
	docker-compose exec influxdb influx

update-monitor-lambda:
	cd temp-logger-monitor; zip ../my-deployment-package.zip monitor.py
	aws lambda update-function-code --function-name temp-sensor-monitor --zip-file fileb://my-deployment-package.zip | cat
FROM arm32v6/python:3.7-alpine

RUN apk --no-cache add git build-base ca-certificates

WORKDIR /app
RUN pip install influxdb
RUN git clone https://github.com/adafruit/Adafruit_Python_DHT.git && \
	cd Adafruit_Python_DHT && \
	python3 setup.py install && \
	cd ..

#RUN git clone https://github.com/pimylifeup/Adafruit_Python_CharLCD.git && \
#	cd Adafruit_Python_CharLCD && \
#	python3 setup.py install  && \
#	cd ..

COPY temp-logger.py temp-logger.py

CMD [ "python", "./temp-logger.py" ]
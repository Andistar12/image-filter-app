.PHONY: built start now

all: stop build start

build: 
	docker build -t web .

start: 
	docker run -p 80:5000 --name web-proj --log-driver local web

stop:
	-docker rm web-proj
	-docker rmi web

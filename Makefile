VERSION=v2
DOCKERUSER=mprach

build:
	docker build -f Dockerfile -t expenselens-microservice .
push:
	docker tag expenselens-microservice $(DOCKERUSER)/expenselens-microservice:$(VERSION)
	docker push $(DOCKERUSER)/expenselens-microservice:$(VERSION)
	docker tag expenselens-microservice $(DOCKERUSER)/expenselens-microservice:latest
	docker push $(DOCKERUSER)/expenselens-microservice:latest

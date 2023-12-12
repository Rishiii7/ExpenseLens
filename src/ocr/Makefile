VERSION=v2
DOCKERUSER=mprach

build:
	docker build -f Dockerfile -t ocr-microservice .
push:
	docker tag ocr-microservice $(DOCKERUSER)/ocr-microservice:$(VERSION)
	docker push $(DOCKERUSER)/ocr-microservice:$(VERSION)
	docker tag ocr-microservice $(DOCKERUSER)/ocr-microservice:latest
	docker push $(DOCKERUSER)/ocr-microservice:latest

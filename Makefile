all: build test clean

build:
	ansible-galaxy install -r requirements.yml -f
	docker build -t curbd-test .

test:
	docker run curbd-test

nose:
	nosetests --with-coverage --cover-inclusive --cover-package=cf

clean:
	docker rmi -f curbformation-test
	rm -r roles
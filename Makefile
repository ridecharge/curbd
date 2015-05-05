all: build test clean

build:
	ansible-galaxy install -r requirements.yml -f
	docker build --pull -t curbd-test .

test:
	docker run curbd-test

nose:
	nosetests --with-coverage --cover-inclusive --cover-package=curbd

clean:
	docker rmi -f curbd-test
	rm -r roles
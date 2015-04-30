FROM registry.gocurb.internal:80/ansible

RUN apt-get update && \
		apt-get -y upgrade && \
		apt-get install -y build-essential
RUN mkdir -p /opt/curbd
WORKDIR /opt/curbd
COPY . .
RUN pip3 install -e .
ENTRYPOINT ["make", "nose"]

FROM ubuntu:20.04

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container


# install dependencies
RUN apt update
RUN apt install default-jre -y
RUN apt install wget -y
RUN wget https://download.opensuse.org/repositories/home:/cabelo/xUbuntu_20.04/amd64/owasp-zap_2.11.1-1_amd64.deb
RUN apt install ./owasp-zap_2.11.1-1_amd64.deb -y
RUN apt install python3 -y
RUN apt install python3-pip -y
# define the port number the container should expose
# run the command
RUN pip3 install python-owasp-zap-v2.4
# RUN owasp-zap -daemon --host 0.0.0.0 --port 8080 -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true -config api.key=changeme
COPY . .
CMD ["./test.sh"]
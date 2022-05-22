
FROM alpine:latest

# set directory for the app
WORKDIR /usr/src/

# copy needed file to the container
COPY . .

# install python3 and pip
RUN apk add python3 && apk add py3-pip

ENTRYPOINT ["sh", "./file.sh"]
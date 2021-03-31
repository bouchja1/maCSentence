# start from base
FROM node:14-alpine3.13 as builder

MAINTAINER Jan Bouchner <jan.bouchner@gmail.com>

RUN apk --no-cache add python make g++

COPY package*.json ./

RUN yarn

# The instructions for second stage
FROM node:14-alpine3.13

WORKDIR /usr/src/app
COPY --from=builder node_modules node_modules

# Bundle app source
COPY . .

# fetch app specific deps
## Add the wait script to the image
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

# expose port
EXPOSE 3001

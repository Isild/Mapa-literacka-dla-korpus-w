FROM node:13.12

WORKDIR /usr/src/app/client
COPY ./ .
RUN yarn install

EXPOSE 8080

ENTRYPOINT [ "yarn", "serve" ]

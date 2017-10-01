# Request Duplicator [![Build Status](https://travis-ci.org/globalgiving/docker-request-duplicator.svg?branch=master)](https://travis-ci.org/globalgiving/docker-request-duplicator)

A docker service that accepts tcp requests and copies them to all instances of a swarm service

Whenever a connection comes in, the request-duplicator will copy that request to every instance of a specified docker swarm service. The response from only one of those instances will be returned to the requester.

## Why would you need this?

At GlobalGiving we use this to send PURGE requests to all of our varnish servers.

This could also be used to duplicate traffic to your production and testing environments if you wanted to check how your test environment handles the same traffic.

## Usage

You must specify the two environment variables `SERVICE_NAME` and `SERVICE_PORT`.  Also, make sure that the request-duplicator runs in the same network as the service you want it to connect to.

```
docker service create \
  --name request-duplicator \
  --mount type=bind,source=/var/run/docker.sock,destination=/var/run/docker.sock \
  --publish 8080:8080 \
  --network varnish-net \
  -e SERVICE_NAME=varnish \
  -e SERVICE_PORT=80 \
  globalgiving/request-duplicator:latest
```

## Environmental variables

You can configure which service the requests are duplicated to with these environement variables:

> **SERVICE_NAME** `varnish`
> **SERVICE_PORT** `80`

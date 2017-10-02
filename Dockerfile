FROM alpine:3.6
MAINTAINER Justin Rupp <jrupp@globalgiving.org>
RUN apk add --update python3 \
     && pip3 install docker \
     && rm -rf /var/cache/apk/*
COPY request-duplicator.py /request-duplicator.py
CMD ["python3", "/request-duplicator.py"]

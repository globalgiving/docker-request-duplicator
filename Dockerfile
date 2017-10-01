FROM python:3.6
RUN pip install docker
COPY request-duplicator.sh /request-duplicator.sh
RUN chmod 755 /request-duplicator.sh
CMD ["/request-duplicator.sh"]

FROM python:3.6
RUN pip install docker
COPY request-duplicator.py /request-duplicator.py
CMD ["python", "/request-duplicator.py"]

FROM python:alpine

RUN pip install clamd
COPY download_and_scan.py /


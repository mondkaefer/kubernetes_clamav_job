FROM python:alpine

RUN pip install kubernetes
COPY inside-clamav-job.py kubernetes_job.py /

CMD ["python3", "/inside-clamav-job.py"]


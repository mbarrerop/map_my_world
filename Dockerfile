FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    gettext \
    postgresql \
    postgresql-contrib \
    postgis \
    && apt-get clean

WORKDIR /src

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

COPY /.env /.env
RUN chmod +x /.env

# healthcheck
COPY /healthcheck.sh /healthcheck.sh
RUN sed -i 's/\r$//g' /healthcheck.sh
RUN chmod +x /healthcheck.sh
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl -f http://0.0.0.0:8000/ || exit 1
# Run application in port 8000
EXPOSE 8000
CMD gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 --max-requests 100 --access-logfile - --error-logfile - --log-level info
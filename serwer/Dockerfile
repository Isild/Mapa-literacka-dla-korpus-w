FROM python:3.6

WORKDIR /usr/src/app/server
COPY ./ .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python", "app_run.py", "run"]

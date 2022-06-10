FROM python:latest
WORKDIR /code
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./ ./
EXPOSE 8050/tcp
CMD ["python", "-u", "app.py"]


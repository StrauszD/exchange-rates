FROM python:3.7

RUN mkdir repo
COPY . repo/
WORKDIR repo

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD python3 app.py
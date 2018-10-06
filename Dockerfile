FROM polyhx/python-seed:2018

ADD . .

EXPOSE 3000

CMD ["python3", "server.py"]

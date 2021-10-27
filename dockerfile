FROM alpine:3.7
RUN apk add --no-cache python3 py-pip3 py-mysqldb
RUN mkdir server_ida
COPY server.py /server_ida/server.py
COPY libraries /server_ida/libraries
COPY static /server_ida/static
COPY template /server_ida/template
RUN pip install -r /server_ida/requirements.txt
EXPOSE 6789
WORKDIR /server_ida
CMD ["python3","server.py"]

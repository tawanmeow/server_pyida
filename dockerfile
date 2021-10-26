FROM alpine:3.7
RUN apk add --no-cache python3
RUN mkdir server_ida
COPY server.py /server_ida/server.py
COPY entes_mpr45s.py /server_ida/entes_mpr45s.py
COPY powermeter69.py /server_ida/powermeter69.py
COPY schneider.py /server_ida/schneider.py
EXPOSE 6789
WORKDIR /server_ida
CMD ["python3","server.py"]

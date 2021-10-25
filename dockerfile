FROM alpine:3.7
RUN apk add --no-cache python3
RUN mkdir ScottishFold
COPY dataset_cm_model.zip /ScottishFold/dataset_cm_model.zip
COPY pcap.zip /ScottishFold/pcap.zip
COPY server.py /ScottishFold/server.py
EXPOSE 6789
WORKDIR /ScottishFold
CMD ["python3","server.py"]

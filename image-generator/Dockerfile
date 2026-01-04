FROM python:alpine

RUN apk add --no-cache bash socat wget curl python3 cups py-pip

RUN addgroup -g 1000 python
RUN adduser -u 1000 -G python -D -s /bin/bash python

#USER python
WORKDIR /app
COPY --chown=python src/ .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "-u", "image_generator.py"]


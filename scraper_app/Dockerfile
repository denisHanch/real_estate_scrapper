FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/parse_real_estate

CMD ["scrapy", "crawl", "realestatespider"]

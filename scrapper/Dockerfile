FROM python:3.10-slim

WORKDIR /scrapper

COPY . /scrapper/

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /scrapper/parse_real_estate

CMD ["scrapy", "crawl", "realestatespider"]

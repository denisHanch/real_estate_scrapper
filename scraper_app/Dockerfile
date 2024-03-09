FROM python:3.10-slim

# READ credentials
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB

# ADD credentials to container environment
ENV POSTGRES_USER $POSTGRES_USER
ENV POSTGRES_PASSWORD $POSTGRES_PASSWORD
ENV POSTGRES_DB $POSTGRES_DB

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/parse_real_estate

CMD ["scrapy", "crawl", "realestatespider"]

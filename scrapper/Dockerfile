FROM python:3.10-slim

WORKDIR /scrapper

COPY . /scrapper/

RUN pip install --no-cache-dir -r requirements.txt


COPY . /scrapper/

CMD ["python", "parse_real_estate.py"]

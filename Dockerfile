FROM python:3.11-slim  AS builder-base

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY . ./

RUN pip install -r requirements.txt

RUN python mkdocs.py

RUN mkdocs build

FROM python:3.11-slim  AS production

WORKDIR /app

COPY --from=builder-base /app/site ./site

EXPOSE 8091

CMD python -m http.server 8091 --directory /app/site
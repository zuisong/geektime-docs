FROM python:3.11-slim  AS builder-base

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY . ./

RUN pip install -r requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN python mkdocs.py

RUN mkdocs build

FROM python:3.11-slim  AS production

WORKDIR /app

RUN pip install fastapi uvicorn requests  -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY --from=builder-base /app/site ./site
ADD  app.py .

EXPOSE 8091

CMD python app.py
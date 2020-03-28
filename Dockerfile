FROM ubuntu:18.04
FROM python:3.6-slim
COPY . /app

WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 8501
CMD [ "streamlit", "run", "api.py" ]


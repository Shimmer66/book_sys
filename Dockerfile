FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /book_sys
#暴露端口
EXPOSE 8080
COPY requirements.txt /book_sys/
RUN pip install -r requirements.txt
COPY . /book_sys/

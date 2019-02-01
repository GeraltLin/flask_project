FROM python:3.5
MAINTAINER linwenxing "linwx.mail@gmail.com"
COPY ./models /root/.keras/models
COPY . /app
WORKDIR /app
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt


ENTRYPOINT ["python"]
CMD ["app.py"]

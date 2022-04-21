FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD ["gunicorn","-w","3","app:app","--bind","0.0.0.0:80"]
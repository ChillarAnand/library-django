from celery import Celery

app = Celery(broker='amqp://guest@localhost//')
app.conf.update(
    result_backend='django-db',
    result_backend_db='db+postgresql://test:test@localhost:5432/test')


@app.task()
def add(x, y):
    return x + y

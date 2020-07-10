import logging
import sys
from math import sqrt
from celery import Celery
from celery.signals import after_setup_logger
import re
import requests

REDIS_URL = 'redis://redis-mq:6379/0'
app = Celery('tasks', broker=REDIS_URL, backend=REDIS_URL)


# To See the startup banner when you execute it by docker container
# See more: https://www.distributedpython.com/2018/10/01/celery-docker-startup/
# @after_setup_logger.connect
# def setup_loggers(logger, *args, **kwargs):
#     logger.addHandler(logging.StreamHandler(sys.stdout))


@app.task
def sqrt_task(value):
    return sqrt(value)


@app.task
def fibo_task(value):
    a, b = 0, 1
    for item in range(value):
        a, b = b, a + b
    message = "The Fibonacci calculated with task id %s was %d" % (fibo_task.request.id, a)
    return value, message


@app.task
def crawl_task(url):
    html_link_regex = re.compile('<a\s(?:.*?\s)*?href=[\'"](.*?)[\'"].*?>')
    request_data = requests.get(url)
    links = html_link_regex.findall(request_data.text)
    message = "The task %s found the following links %s.." % (crawl_task.request.id, links)
    return message


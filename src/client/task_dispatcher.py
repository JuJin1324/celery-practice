# Created by Yoo Ju Jin(jujin@100fac.com) 
# Created Date : 2020/07/09
# Copyright (C) 2020, Centum Factorial all rights reserved.
import logging
import sys
from celery import Celery

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

REDIS_URL = 'redis://redis-mq:6379/0'
app = Celery('tasks', broker=REDIS_URL, backend=REDIS_URL)


def manage_sqrt_task(value):
    result = app.send_task('tasks.sqrt_task', args=(value,), queue='sqrt_queue', routing_key='sqrt_queue')
    logging.info(f"result.get(): {result.get()}")


def manage_fibo_task(value_list):
    async_result_dict = {x: app.send_task('tasks.fibo_task', args=(x,), queue='fibo_queue', routing_key='fibo_queue')
                         for x in value_list}
    for key, value in async_result_dict.items():
        if value.ready():
            logging.info("Value [%d] -> %s" % (key, value.get()[1]))
        else:
            logging.info("Task [%s] is not ready" % value.task_id)


def manage_crawl_task(url_list):
    async_result_dict = {
        url: app.send_task('tasks.crawl_task', args=(url,), queue='webcrawler_queue', routing_key='webcrawler_queue')
        for url in url_list
    }
    for key, value in async_result_dict.items():
        logging.info("%s -> %s" % (key, value.get(timeout=7)))
    # if value.ready():
    #     logging.info("%s -> %s" % (key, value.get(timeout=7)))
    # else:
    #     logging.info("The task [%s] is not ready" % value.task_id)


if __name__ == '__main__':
    # manage_sqrt_task(16)
    #
    # input_list = [4, 3, 8, 6, 10]
    # manage_fibo_task(input_list)

    url_list = [
        'http://www.google.com',
        'http://br.bing.com',
        'http://duckduckgo.com',
        'http://github.com',
        'http://br.search.yahoo.com'
    ]
    manage_crawl_task(url_list)

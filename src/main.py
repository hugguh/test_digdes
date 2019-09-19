import aiohttp_jinja2
import aiohttp
import jinja2
from aiohttp import web
import asyncio
import logging
import colorlog

import traceback
from dotenv import load_dotenv
import os

async def start(app):
    log_1 = app['logging']

async def main_page(request):
    app = request.app
    log = app['logging']
    log.warning("main page open")
    data_page = {"error": ""}
    response = aiohttp_jinja2.render_template('main.html', request, data_page)
    return response


def main():
    loop = asyncio.get_event_loop()
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates/'))  # setup jinja2 environment
    app.router.add_get('/', main_page)
    app.router.add_static('/static/', path='./static/', name='static')
    app.router.add_get('/{tail:.*}', main_page)

    # init logger
    log = colorlog.getLogger('log')
    # format of logs
    formatter = colorlog.ColoredFormatter('%(log_color)s%(asctime)s %(levelname)s: %(message)s (%(module)s:%(lineno)d)')
    # set loglevel
    log_level = logging.INFO
    log.setLevel(log_level)
    # set stream logging settings
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    log.addHandler(ch)


    app['logging'] = log
    log.warning("log_init")
    env_path = '../.env'
    load_dotenv(dotenv_path=env_path)
    app['host'] = os.getenv("HOST")
    app['port'] = int(os.getenv("PORT"))
    loop.run_until_complete(start(app))
    web.run_app(app, host=app['host'], port=app['port'])


if __name__ == '__main__':
    main()
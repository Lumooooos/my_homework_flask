#sqlite3是一款轻量级数据库，支持sql语句
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

#建立数据库连接
def get_db():
    #g 是一个特殊对象，独立于每一个请求。
    #g 可以多次使用，而不用在同一个请求中每次调用 get_db 时都创建一个新的连接。
    if 'db' not in g:
        #连接数据库
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


#关闭数据库连接
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        #关闭连接
        db.close()
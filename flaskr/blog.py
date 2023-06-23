from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

#博客蓝图
bp = Blueprint('blog', __name__)

#建立了一个索引，将最新的帖子排在最前面
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

# 新建
# 帖子详情
@bp.route('/post/<int:post_id>')
def post(post_id):
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    for p in posts:
        if p['id'] == post_id:
            return render_template('blog/post.html', post=p)
    return '未找到该帖子'

#创建新的帖子
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        #新增，对于敏感词的屏蔽的调用
        title = check_sensitive_words(title)
        body = check_sensitive_words(body)

        #检测帖子是否有标题
        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)

        else:
        #没有错误的话，将帖子的标题，主题，作者id都插入到数据库中，即视为发帖成功
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')



#新增
#设置敏感词
sensitive_words = ['习近平','杀','死']

#对于新建的帖子以及修改帖子的时候，会检测帖子的主题和内容中是否存在敏感词
def check_sensitive_words(s):
    for word in sensitive_words:
        s = s.replace(word,'*' * len(word))
    return s




#检测帖子是否存在，检测当前用户是否为帖子作者
#主要用于更新帖子之前
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


#更新帖子
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        #新增，对于敏感词的屏蔽的调用
        title = check_sensitive_words(title)
        body = check_sensitive_words(body)

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)


        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


#删除帖子
#由于删除帖子对应的按钮已经存在于更新（update.html）中，因此删除操作没有专门对应一个Html文件
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
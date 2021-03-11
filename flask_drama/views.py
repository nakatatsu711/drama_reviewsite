from flask import render_template
from flask import redirect
from flask import session
from flask import flash
from flask import url_for
from flask import request
from flask_drama import app
from flask_drama import db
from flask_drama.models.users import User
from flask_drama.models.dramas import Drama
from flask_drama.models.posts import Post
from sqlalchemy.exc import IntegrityError
from random import sample


@app.route('/')
def index():
    dramas = Drama.query.all()
    dramas = sample(dramas, len(dramas))
    review_rankings = Drama.query.order_by(Drama.mean.desc()).all()
    rate_rankings = Drama.query.order_by(Drama.rate.desc()).all()
    return render_template('index.html', dramas=dramas, review_rankings=review_rankings, rate_rankings=rate_rankings)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not request.form['username'] and not request.form['password']:
            flash('ユーザー名を入力してください')
            flash('パスワードを入力してください')
            return render_template('login.html', username=request.form['username'], password=request.form['password'])
        if not request.form['username']:
            flash('ユーザー名を入力してください')
            return render_template('login.html', username=request.form['username'], password=request.form['password'])
        if not request.form['password']:
            flash('パスワードを入力してください')
            return render_template('login.html', username=request.form['username'], password=request.form['password'])
        users_model = User.query.all()
        for user_model in users_model:
            if request.form['username'] == user_model.username:
                if request.form['password'] == user_model.password:
                    session['logged_in'] = True
                    flash('ログインしました')
                    if user_model.username == 'nakatatsu':
                        session['admin_name'] = True
                    return redirect(url_for('index'))
                flash('パスワードが異なります')
                return render_template('login.html', username=request.form['username'], password=request.form['password'])
        flash('ログインできません')
        return render_template('login.html', username=request.form['username'], password=request.form['password'])
    else:
        return render_template('login.html', username='', password='')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('admin_name', None)
    flash('ログアウトしました')
    return redirect(url_for('index'))

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        try:
            user = User(
                username=request.form['username'],
                password=request.form['password']
            )
            if not user.username and not user.password:
                flash('ユーザー名を入力してください')
                flash('パスワードを入力してください')
                return render_template('new.html', user=user)
            if not user.username:
                flash('ユーザー名を入力してください')
                return render_template('new.html', user=user)
            if not user.password:
                flash('パスワードを入力してください')
                return render_template('new.html', user=user)
            db.session.add(user)
            db.session.commit()
            session['logged_in'] = True
            flash('登録しました')
            if user.username == 'nakatatsu':
                session['admin_name'] = True
            return redirect(url_for('index'))
        except IntegrityError:
            flash('ユーザー名が既に使用されています')
            return render_template('new.html', user=user)
    else:
        user = User()
        return render_template('new.html', user=user)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        try:
            drama = Drama(
                title=request.form['admin-title'],
                actor=request.form['actor'],
                rate=request.form['rate']
            )
            if not drama.title and not drama.actor and not drama.rate:
                flash('ドラマのタイトルを入力してください')
                flash('出演者を入力してください')
                flash('視聴率を入力してください')
                return render_template('admin.html', drama=drama)
            if not drama.title and not drama.actor:
                flash('ドラマのタイトルを入力してください')
                flash('出演者を入力してください')
                return render_template('admin.html', drama=drama)
            if not drama.title and not drama.rate:
                flash('ドラマのタイトルを入力してください')
                flash('視聴率を入力してください')
                return render_template('admin.html', drama=drama)
            if not drama.actor and not drama.rate:
                flash('出演者を入力してください')
                flash('視聴率を入力してください')
                return render_template('admin.html', drama=drama)
            if not drama.title:
                flash('ドラマのタイトルを入力してください')
                return render_template('admin.html', drama=drama)
            if not drama.actor:
                flash('出演者を入力してください')
                return render_template('admin.html', drama=drama)
            if not drama.rate:
                flash('視聴率を入力してください')
                return render_template('admin.html', drama=drama)
            db.session.add(drama)
            db.session.commit()
            flash('入力しました')
            return redirect(url_for('admin'))
        except IntegrityError:
            flash('このドラマは既に入力されています')
            return render_template('admin.html', drama=drama)
    else:
        drama = Drama()
        return render_template('admin.html', drama=drama)

@app.route('/posts')
def posts_index():
    dramas = Drama.query.order_by(Drama.title.asc()).all()
    return render_template('posts_index.html', dramas=dramas)

@app.route('/posts/<int:id>', methods=['GET', 'POST'])
def posts_detail(id):
    if request.method == 'POST':
        post = Post(
            drama_id=id,
            star=request.form['star'],
            review=request.form['review-input']
        )
        drama = Drama.query.get(id)
        if not post.star and not post.review:
            flash('評価を選択してください')
            flash('レビューを入力してください')
            return render_template('posts_detail.html', drama=drama, post=post)
        if not post.star:
            flash('評価を選択してください')
            return render_template('posts_detail.html', drama=drama, post=post)
        if not post.review:
            flash('レビューを入力してください')
            return render_template('posts_detail.html', drama=drama, post=post)
        db.session.add(post)
        db.session.commit()
        total = 0
        num = 0
        for post in drama.posts:
            total += post.star
            num += 1
        drama.mean = round((total / num), 2)
        db.session.merge(drama)
        db.session.commit()
        flash('投稿しました')
        return redirect(url_for('posts_detail', id=id))
    else:
        drama = Drama.query.get(id)
        post = Post()
        return render_template('posts_detail.html', drama=drama, post=post)

@app.route('/posts/<int:id>/delete')
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    flash('削除しました')
    drama_id = post.drama_id
    return redirect(url_for('posts_detail', id=drama_id))

@app.route('/posts/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        drama = Drama.query.get(id)
        if not request.form['rate']:
            flash('視聴率を入力してください')
            return render_template('update.html', drama=drama)
        drama.rate = request.form['rate']
        db.session.merge(drama)
        db.session.commit()
        flash('視聴率を変更しました')
        return redirect(url_for('posts_detail', id=drama.id))
    else:
        drama = Drama.query.get(id)
        return render_template('update.html', drama=drama)

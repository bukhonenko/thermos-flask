import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# @TODO for debug mode
from logging import DEBUG

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '1Q'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
# sqlite:////home/mgu/Python/thermos/thermos-flask/thermos.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# @TODO Debug for manage.py runserver
app.config['DEBUG'] = True

db = SQLAlchemy(app)

from forms import BookmarkForm
import models

# @TODO for debug mode
app.logger.setLevel(DEBUG)


# Fake login
def logged_user():
    return models.User.query.filter_by(username='alex').first()


@app.route('/')
@app.route('/index')
def index():
    # app.logger.debug(app.config)  # @TODO print in debug mode
    return render_template('index.html', new_bookmarks=models.Bookmark.newest(5))

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        bm = models.Bookmark(user=logged_user(), url=url, description=description)
        db.session.add(bm) # TODO the object has been aleady added through manage.initdb
        db.session.commit()
        flash('Stored bookmark "{}"'.format(url))
        app.logger.debug('strored url: ' + url) # @TODO print in debug mode
        return redirect(url_for('index'))
    return render_template('add.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
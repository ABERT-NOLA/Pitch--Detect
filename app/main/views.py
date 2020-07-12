from os import abort

from flask import render_template, redirect, url_for, request
from flask_login import login_required

from app import db, photos
from app.main import main
from app.main.forms import UpdateProfile
from app.models import User


@main.route('/')
def index():
    return render_template("index.html")


# =========== User profile ==================

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)


def get_upload_path(filename):
    """
    Creates path to the uploads folder.
    :param filename:
    :return:
    """
    return f'uploads/photos/{filename}'


@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = get_upload_path(filename)
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))

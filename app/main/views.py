from os import abort

import markdown2
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user

from app import db, photos, audio
from app.main import main
from app.main.forms import UpdateProfile, ReviewForm, PitchForm, VoteForm, CategoryForm
from app.models import User, Pitch, Review, Vote, Category


@main.route('/')
@login_required
def pitches():
    return render_template("pitch/pitches.html", pitches=Pitch.query.all(), title="Pitches")


# =========== Pitch Category==================

@main.route('/categories', methods=['GET'])
@login_required
def categories():
    return render_template("pitch/categories.html", categories=Category.query.all(), title="Categories")


@main.route('/category', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        # Updated review instance
        category = Category(
            name=name
        )

        # save review method
        category.save_category()
        return redirect(url_for('.categories'))

    title = f'New Category'
    return render_template('pitch/new_category.html', title=title, form=form)


@main.route('/category/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_category(id):
    category = Category.query.get(id)
    form = CategoryForm(formdata=request.form, obj=category)
    if form.validate_on_submit():
        name = form.name.data
        # Updated review instance
        category.name = name
        # save review method
        category.save_category()
        return redirect(url_for('.categories'))

    title = f'Update Pitch'
    return render_template('pitch/new_category.html', title=title, form=form)


@main.route('/category/<int:id>')
@login_required
def single_category(id):
    category = Category.query.get(id)
    if category is None:
        abort(404)
    return render_template(
        'pitch/category.html',
        category=category,
        pitches=Pitch.query.filter_by(category_id=category.id).all()
    )


# =========== Pitch==================

@main.route('/pitch', methods=['GET', 'POST'])
@login_required
def new_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        category = form.category.data

        # Updated review instance
        pitch = Pitch(
            name=name,
            description=description,
            owner_id=current_user.id
        )
        pitch.category_id = category.id
        # save review method
        pitch.save_pitch()
        return redirect(url_for('.single_pitch', id=pitch.id))

    title = f'New Pitch'
    return render_template('pitch/new_pitch.html', title=title, form=form)


@main.route('/pitch/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_pitch(id):
    pitch = Pitch.query.get(id)
    form = PitchForm(formdata=request.form, obj=pitch)
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        category = form.category.data
        # Updated review instance
        pitch.name = name
        pitch.description = description
        pitch.category_id = category.id
        # save review method
        pitch.save_pitch()
        return redirect(url_for('.single_pitch', id=pitch.id))

    title = f'Update Pitch'
    return render_template('pitch/new_pitch.html', title=title, form=form)


@main.route('/pitch/<int:id>/update/audio', methods=['POST'])
@login_required
def pitch_audio(id):
    pitch = Pitch.query.get(id)
    if 'audio' in request.files:
        filename = audio.save(request.files['audio'])
        path = get_upload_audio_path(filename)
        pitch.audio_url = path
        db.session.commit()
    return redirect(url_for('main.single_pitch', id=id))


@main.route('/pitch/<int:id>')
@login_required
def single_pitch(id):
    pitch = Pitch.query.get(id)
    if pitch is None:
        abort(404)
    reviews = Review.get_reviews(pitch.id)
    vote_count = Vote.get_vote_count(pitch.id)
    vote_dict = {}
    for type, count in vote_count:
        vote_dict[type] = count
    return render_template(
        'pitch/pitch.html',
        pitch=pitch,
        vote_count=vote_dict,
        reviews=reviews,
        reviewform=ReviewForm(),
        voteform=VoteForm()
    )


# =========== Pitch Vote==================
@main.route('/pitch/<int:id>/vote', methods=['POST'])
def pitch_vote(id):
    pitch = Pitch.query.get(id)
    vote = Vote.query.filter_by(user_id=current_user.id, pitch_id=pitch.id).first()
    print(vote)
    if not vote:
        vote = Vote(type=vote, pitch_id=id)
    form = VoteForm()
    if form.validate_on_submit():
        vote.type = form.type.data
    vote.save_vote()
    return redirect(url_for('.single_pitch', id=pitch.id))


# =========== Pitch Reviews==================

@main.route('/pitch/<int:id>/review', methods=['GET', 'POST'])
@login_required
def new_review(id):
    form = ReviewForm()
    pitch = Pitch.query.get(id)
    if form.validate_on_submit():
        review = form.review.data

        # Updated review instance
        user_review = Review(
            pitch_id=pitch.id,
            pitch_review=review,
            user_id=current_user.id
        )

        # save review method
        user_review.save_review()
        return redirect(url_for('.single_pitch', id=pitch.id))

    title = f'{pitch.name} review'
    return render_template('pitch/new_review.html', title=title, review_form=form, pitch=pitch)


@main.route('/review/<int:id>')
def single_review(id):
    review = Review.query.get(id)
    if review is None:
        abort(404)
    format_review = markdown2.markdown(review.movie_review, extras=["code-friendly", "fenced-code-blocks"])
    return render_template('pitch/review.html', review=review, format_review=format_review)


# =========== User profile ==================

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user, pitches=Pitch.query.filter_by(owner_id=user.id).all())


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


def get_upload_photo_path(filename):
    """
    Creates path to the uploads folder.
    :param filename:
    :return:
    """
    return f'uploads/photos/{filename}'


def get_upload_audio_path(filename):
    """
    Creates path to the uploads folder.
    :param filename:
    :return:
    """
    return f'uploads/audio/{filename}'


@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = get_upload_photo_path(filename)
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))

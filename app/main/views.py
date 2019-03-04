from flask import render_template,request,redirect,url_for,abort
from . import main

from .forms import ReviewForm,UpdateProfile
from ..models import Review
from .forms import PostsForm,CommentForm
from ..models import User,Pitches,Comment
from flask_login import login_required,current_user
from .. import db, photos



@main.route('/')
def index():

    title = 'Home - Welcome to The best Movie Review Website Online'
    return render_template('index.html', title = title )
@main.route('/movies/<int:id>')
def movies(movie_id):

    '''
    View movie page function that returns the movie details page and its data
    '''
    return render_template('movie.html',id = movie_id)


@main.route('/movie/review/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_review(id):
    form = ReviewForm()
    movie = get_movie(id)

    if form.validate_on_submit():
        title = form.title.data
        review = form.review.data
        new_review = Review(movie.id,title,movie.poster,review)
        new_review.save_review()
        return redirect(url_for('main.movie',id = movie.id ))

    title = f'{movie.title} review'
    return render_template('new_review.html',title = title, review_form=form, movie=movie)

@main.route('/user/<uname>',methods = ["GET","POST"])
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    
    # form=PostsForm(form.description.data)
    # description=form.description.data
    # form=CommentForm()
    form = CommentForm()
    pitches=Pitches.fetch_pitches()
    if form.validate_on_submit():
        comment=Comment(comment=form.comment.data,user_id=current_user.id)#,pitch_id=pitch_id
        db.session.add(comment)
        db.session.commit()
        comment.save_comment()
        # return redirect(url_for('.index'))
  
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,opinion=form,pitches=pitches)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)
    

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))    


# @main.route('/posts/<int:id>')
# def posts(posts_id):

#     '''
#     View posts
#     '''
#     if user is None:
#         abort(404)

#     user = User.query.filter_by(id = posts_id).first()

#     return render_template('posts.html',user = user)

# @main.route('/movie/posts/<int:id>', methods = ['GET','POST'])
# # @app.route('/movie/review/new/<int:id>', methods = ['GET','POST'])
# @login_required

# def posts():
#     form = PostsForm()
#     # movie=PostsCategory.query.filter_by(id=id).first()
#     title = "Posts Area"
    
#     # if movie is None:
#     #     abort(404)

#     # if  posts_form.validate_on_submit():
#     #     content =  posts_form.content.data
#     #     # review = posts_form.review.data
#     #     new_post = PostsForm(content=content)
#     #     new_post.save_post()
#     #     return redirect(url_for('.movie',id = movie.id ))

#     # title = f'{movie.title} review'
#     return render_template('posts.html',posts_form = posts_form,title=title)
#     # return render_template('new_review.html',title = title, review_form=form, movie=movie)

#Category routing
# @main.route('/education')
# def education():

#     '''
#     Category route
#     '''
#     if user is None:
#         abort(404)

#     user = User.query.filter_by(id = posts_id).first()

#     return render_template('posts.html',user = user)

#Pitch routing
@main.route('/posts',methods = ["GET","POST"])
@login_required
def posts():
    form = PostsForm()
   
    if form.validate_on_submit():
        posted=Pitches(description=form.description.data,user_id=current_user.id)
        db.session.add(posted)
        db.session.commit()
        posted.save_post()
        return redirect(url_for('.index'))
        print(posted)
    return render_template('posts.html',posts_form = form)

#Comment routing
# @main.route('/comments',methods = ["GET","POST"])
# @login_required
# def comments():
#     form = CommentForm()
   
#     if form.validate_on_submit():
#         comment=Comment(comment=form.comment.data,user_id=current_user.id,pitch_id=current_user.id)
#         db.session.add(comment)
#         db.session.commit()
#         comment.save_comment()
#         # return redirect(url_for('.index'))
#     return render_template('profile.html',opinion = form)    
from flask_app import app
from flask import render_template,redirect,request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.topic import Topic
from flask_app.models.idea import Idea
from flask_app.models.comment import Comment
bcrypt = Bcrypt(app)


@app.route("/")
def log_and_reg():
    return render_template("register_and_login.html")

@app.route("/process-register", methods=['POST'])
def process_register():
    if not User.validate_user_for_registration(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    confirm_pw_hash = bcrypt.generate_password_hash(request.form['confirm_password'])
    data1 = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash,
        'confirm_password': confirm_pw_hash
    }
    id = User.save_into_db(data1)
    data2 = {
        'id': id
    }
    user = User.get_by_id(data2)
    session['id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    return redirect("/dashboard")

@app.route("/process-login", methods=['POST'])
def process_login():
    data = {
        'email': request.form['email'],
        'password': request.form['password']
    }
    user_in_db = User.get_by_email(data)
    if not User.validate_user_for_login(data):
        return redirect('/')
    print(user_in_db.password)
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash(u"Invalid password", 'login_error')
        return redirect('/')
    user = User.get_by_email(data)
    session['id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    return redirect('/dashboard')

@app.route('/user/<int:user_id>')
def show_profile_of_user(user_id):
    data = {
        'id': user_id
    }
    topics = Topic.get_all_topics()
    user_with_owned_ideas = User.get_user_owned_ideas(data)
    for idea in user_with_owned_ideas.ideas:
        data1 = {
            "id" : idea.id
        }
        liked_by = Idea.get_likes_of_idea(data1)
        idea.n_likes = len(liked_by)
        idea.liked_by = liked_by
        idea.liked_by_ids = []
        for like in liked_by:
            idea.liked_by_ids.append(like.id)
    for idea in user_with_owned_ideas.ideas:
        data2 = {
            "id" : idea.id
        }
        comments = Comment.get_comments_of_idea(data2)
        idea.comments = comments
        idea.n_comments = len(comments)
    user_with_liked_ideas = User.get_user_with_ideas_liked(data)
    for idea in user_with_liked_ideas.ideas_liked:
        data3 = {
            "id" : idea.id
        }
        liked_by = Idea.get_likes_of_idea(data3)
        idea.n_likes = len(liked_by)
        idea.liked_by = liked_by
        idea.liked_by_ids = []
        for like in liked_by:
            idea.liked_by_ids.append(like.id)
    for idea in user_with_liked_ideas.ideas_liked:
        data4 = {
            "id" : idea.id
        }
        comments = Comment.get_comments_of_idea(data4)
        idea.comments = comments
        idea.n_comments = len(comments)

    topics_liked = Topic.get_topics_liked_by_user(data)
    return render_template('profile.html', user_with_owned_ideas = user_with_owned_ideas, user_with_liked_ideas = user_with_liked_ideas, topics = topics, topics_liked = topics_liked)

@app.route('/process-logout')
def process_logout():
    session.clear()
    return redirect('/')

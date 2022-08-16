from flask_app import app
from flask import render_template,redirect,request, flash, session
from flask_app.models.idea import Idea
from flask_app.models.topic import Topic
from flask_app.models.comment import Comment
import re

@app.route("/dashboard")
def dashboard():
    if not session:
        flash(u"There's no user logged in!", "general_error")
        return redirect('/')
    ideas = Idea.get_ideas_with_users_and_topics()
    topics = Topic.get_all_topics()

    for idea in ideas:
        data = {
            "id" : idea.id
        }
        liked_by = Idea.get_likes_of_idea(data)
        idea.n_likes = len(liked_by)
        idea.liked_by = liked_by
        idea.liked_by_ids = []
        for like in liked_by:
            idea.liked_by_ids.append(like.id)
            # print(like.id)
    for idea in ideas:
        data = {
            "id" : idea.id
        }
        # comments = Idea.get_idea_with_comments(data)
        comments = Comment.get_comments_of_idea(data)
        idea.comments = comments
        idea.n_comments = len(comments)
    return render_template("dashboard.html", ideas = ideas, topics = topics )

@app.route("/idea/create")
def render_idea_create():
    if not session:
        flash(u"There's no user logged in!", "general_error")
        return redirect('/')
    topics = Topic.get_all_topics()
    return render_template("creating_idea.html", topics = topics)

@app.route("/creating-idea", methods=['POST'])
def creating_idea():
    data = {
        'title': request.form['title'],
        'idea_description': request.form['idea_description'],
        'idea_expanded': request.form['idea_expanded'],
        'topic_id': request.form['topic_id'],
        'user_id': session['id'],
    }
    if not Idea.validate_idea(data):
        return redirect('/idea/create')
    Idea.save_into_db(data)
    return redirect('/dashboard')

@app.route("/delete-idea-<int:idea_id>")
def deleting_idea(idea_id):
    data = {
        'id': idea_id
    }
    idea = Idea.get_one_idea_with_user(data)
    if not session['id'] == idea.user_id:
        return redirect('/dashboard')
    Idea.delete_idea(data)
    return redirect('/dashboard')

@app.route("/idea/<int:idea_id>")
def show_one_idea(idea_id):
    data = {
        'id': idea_id
    }
    idea = Idea.get_one_idea_with_user(data)
    topics = Topic.get_all_topics()
    liked_by = Idea.get_likes_of_idea(data)
    idea.n_likes = len(liked_by)
    idea.liked_by = liked_by
    idea.liked_by_ids = []
    for like in liked_by:
        idea.liked_by_ids.append(like.id)
        # print(like.id)
    
    comments = Comment.get_comments_of_idea(data)
    idea.n_comments = len(comments)
    for comment in comments:
        data2 = {
            'id': comment.id
        }
        comment.liked_by_ids = []
        liked_by = Comment.get_likes_of_comment(data2)
        comment.liked_by = liked_by
        # print(liked_by)
        comment.n_likes = len(liked_by)
        for like in liked_by:
            comment.liked_by_ids.append(like.id)
            # print(like.id)
    idea.comments = comments
    return render_template("one_idea.html", idea = idea, topics = topics)


@app.route('/search-for-idea', methods=['POST'])
def search_for():
    if not request.form['search_for']:                  #1 Esto hace que si no hayas buscado nada, redireccione al dashboard
        return redirect('/dashboard')
    data = request.form['search_for']
    all_ideas = Idea.get_ideas_with_users_and_topics()     #2 Aqui saco todas las ideas 
    matching_ideas = []                                    #5 Este array con todas las ideas que coincidieron con lo buscado es el que termino pasando al render template html
    for idea in all_ideas:                                 #3 Aqui hago un for loop para cada idea de entre todas
        if re.search(f'((?i){data}(?i))', idea.idea_description):   #4 Aqui lo que hago es ver si coinciden lo que se buscó, o sea data = request.form['search_for'] con la 
            matching_ideas.append(idea)                                      #  descripcion de cada idea. Si coinciden, meto esta idea al array de la linea 109 
    topics = Topic.get_all_topics()                     #Lo de los topics no le hagas caso, es otra cosa que no tiene que ver xd
    return render_template('dashboard.html', ideas = matching_ideas, topics = topics)





@app.route("/delete-like-idea-<int:idea_id>-user-<int:session_id>")
def delete_idea_like(idea_id, session_id):
    if session['id'] != session_id:
        return redirect('/dashboard')
    data = {
        'idea_id': idea_id,
        'user_id': session_id
    }
    Idea.delete_like_of_idea(data)
    return redirect('/dashboard')

@app.route("/create-like-idea-<int:idea_id>-user-<int:session_id>")
def create_idea_like(idea_id, session_id):
    if session['id'] != session_id:
        return redirect('/dashboard')
    data = {
        'idea_id': idea_id,
        'user_id': session_id
    }
    Idea.create_like_of_idea(data)
    return redirect('/dashboard')


@app.route("/delete-like-idea-<int:idea_id>-user-<int:session_id>-redirect_to_self")
def delete_idea_like_but_redirect_to_self(idea_id, session_id):
    if session['id'] != session_id:
        return redirect(f'/idea/{idea_id}')
    data = {
        'idea_id': idea_id,
        'user_id': session_id
    }
    Idea.delete_like_of_idea(data)
    return redirect(f'/idea/{idea_id}')

@app.route("/create-like-idea-<int:idea_id>-user-<int:session_id>-redirect_to_self")
def create_idea_like_but_redirect_to_self(idea_id, session_id):
    if session['id'] != session_id:
        return redirect(f'/idea/{idea_id}')
    data = {
        'idea_id': idea_id,
        'user_id': session_id
    }
    Idea.create_like_of_idea(data)
    return redirect(f'/idea/{idea_id}')
    
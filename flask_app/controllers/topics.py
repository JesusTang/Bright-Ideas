from flask_app import app
from flask import render_template,redirect,request, flash, session
from flask_app.models.user import User
from flask_app.models.topic import Topic
from flask_app.models.idea import Idea
from flask_app.models.comment import Comment

@app.route('/topic/<int:topic_id>')
def show_ideas_of_one_topic(topic_id):
    if not session:
        flash(u"There's no user logged in!", "general_error")
        return redirect('/')
    data = {
        'id': topic_id
    }
    topic = Topic.get_one_topic_with_ideas(data)
    topics = Topic.get_all_topics()
    topic.n_ideas = len(topic.ideas)
    for idea in topic.ideas:
        data1 = {
            "id" : idea.id
        }
        liked_by = Idea.get_likes_of_idea(data1)
        idea.n_likes = len(liked_by)
        idea.liked_by = liked_by
        idea.liked_by_ids = []
        for like in liked_by:
            idea.liked_by_ids.append(like.id)
            # print(like.id)
    for idea in topic.ideas:
        data2 = {
            "id" : idea.id
        }
        # comments = Idea.get_idea_with_comments(data)
        comments = Comment.get_comments_of_idea(data2)
        idea.comments = comments
        idea.n_comments = len(comments)
    
    liked_by = Topic.get_likes_of_topic(data)
    topic.n_likes = len(liked_by)
    topic.liked_by = liked_by
    topic.liked_by_ids = []
    for like in liked_by:
        print(like.id)
        topic.liked_by_ids.append(like.id)
    return render_template('one_topic_ideas.html', topic = topic, topics = topics)

@app.route("/delete-like-topic-<int:topic_id>-user-<int:session_id>")
def delete_like_topic(topic_id, session_id):
    if session['id'] != session_id:
        return redirect('/dashboard')
    data = {
        'topic_id': topic_id,
        'user_id': session_id
    }
    Topic.delete_like_of_topic(data)
    return redirect(f'/topic/{topic_id}')

@app.route("/create-like-topic-<int:topic_id>-user-<int:session_id>")
def create_like_topic(topic_id, session_id):
    if session['id'] != session_id:
        return redirect('/dashboard')
    data = {
        'topic_id': topic_id,
        'user_id': session_id
    }
    Topic.create_like_of_topic(data)
    return redirect(f'/topic/{topic_id}')
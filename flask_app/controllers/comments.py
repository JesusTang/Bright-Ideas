from flask_app import app
from flask import render_template,redirect,request, flash, session
from flask_app.models.idea import Idea
from flask_app.models.topic import Topic
from flask_app.models.comment import Comment


@app.route("/delete-like-comment-<int:comment_id>-user-<int:session_id>-<int:idea_id>")
def delete_comment_like(comment_id, session_id, idea_id):
    if session['id'] != session_id:
        return redirect(f'/idea/{idea_id}')
    data = {
        'comment_id': comment_id,
        'user_id': session_id
    }
    Comment.delete_like_of_comment(data)
    return redirect(f'/idea/{idea_id}')

@app.route("/create-like-comment-<int:comment_id>-user-<int:session_id>-<int:idea_id>")
def create_comment_like(comment_id, session_id, idea_id):
    if session['id'] != session_id:
        return redirect(f'/idea/{idea_id}')
    data = {
        'comment_id': comment_id,
        'user_id': session_id
    }
    Comment.create_like_of_comment(data)
    return redirect(f'/idea/{idea_id}')

@app.route("/creating-comment-for-idea-<int:idea_id>", methods=['POST'])
def creating_comment(idea_id):
    if not session['id']:
        return redirect('/dashboard')
    data = {
        'comment_description': request.form['comment_description'],
        'idea_id': idea_id,
        'user_id': session['id'],
    }
    Comment.add_comment(data)
    return redirect(f'/idea/{idea_id}')

@app.route("/delete-comment-<int:comment_id>")
def deleting_comment(comment_id):
    data = {
        'id': comment_id
    }
    comment = Comment.get_comment_with_user(data)
    if not session['id'] == comment.user_id:
        return redirect('/dashboard')
    Comment.delete_comment(data)
    return redirect(f'/idea/{comment.idea_id}')

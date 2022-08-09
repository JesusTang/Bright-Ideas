from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from flask_app.models import idea
import re

GENRE_REGEX = re.compile(r'^[a-zA-Z]') 

class Comment:
    def __init__( self , data ):
        self.id = data['id']
        self.comment_description = data['comment_description']
        self.idea_id = data['idea_id']
        self.user_id = data['user_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.liked_by = []

    @classmethod
    def get_comments_with_users( cls ):
        query = """
        SELECT * FROM comments 
        JOIN users ON comments.user_id = users.id;"""
        results = connectToMySQL('bright_ideas').query_db( query )
        comments = []
        for comment in results:
            comments.append(cls(comment))
        return comments

    @classmethod
    def get_comment_with_user( cls , data ):
        query = """
        SELECT * FROM comments 
        LEFT JOIN users ON comments.user_id = users.id
        LEFT JOIN ideas ON comments.idea_id = ideas.id
        WHERE comments.id = %(id)s;"""
        results = connectToMySQL('bright_ideas').query_db( query , data )
        comment = cls(results[0])
        return comment

    @classmethod
    def get_comments_of_idea( cls , data ):
        query = """
        SELECT * FROM comments 
        JOIN users ON comments.user_id = users.id
        JOIN ideas ON comments.idea_id = ideas.id
        WHERE ideas.id = %(id)s;"""
        results = connectToMySQL('bright_ideas').query_db( query , data )
        comments = []
        for comment in results:
            comments.append(cls(comment))
        return comments

    @classmethod
    def get_likes_of_comment( cls , data ):
        query = """
        SELECT * FROM comments_likes 
        JOIN users ON comments_likes.user_id = users.id
        JOIN comments ON comments_likes.comment_id = comments.id
        WHERE comments.id = %(id)s;"""
        results = connectToMySQL('bright_ideas').query_db( query , data )
        likes = []
        for like in results:
            data = {
                'id': like['id'],
                'first_name': like['first_name'],
                'last_name': like['last_name'],
                'email': like['email'],
                'password': like['password'],
                'updated_at': like['updated_at'],
                'created_at': like['created_at'],
            }
            # print(like)
            likes.append(user.User(data))
        return likes

    @classmethod
    def add_comment(cls, data ):
        query = """
        INSERT INTO comments ( comment_description , user_id , idea_id ) 
        VALUES ( %(comment_description)s , %(user_id)s , %(idea_id)s );"""
        result_id = connectToMySQL('bright_ideas').query_db( query, data )
        return result_id

    @classmethod
    def delete_comment(cls, data ):
        query = """
        DELETE FROM comments WHERE id = %(id)s;"""
        result_is_none = connectToMySQL('bright_ideas').query_db( query, data )
        return result_is_none

    @classmethod
    def delete_like_of_comment( cls , data ):
        query = """
        DELETE FROM comments_likes WHERE comment_id = %(comment_id)s AND user_id = %(user_id)s
        """
        results = connectToMySQL('bright_ideas').query_db( query , data)
        return results

    @classmethod
    def create_like_of_comment( cls , data ):
        query = """
        INSERT INTO comments_likes (comment_id, user_id) VALUES (%(comment_id)s ,  %(user_id)s)
        """
        results = connectToMySQL('bright_ideas').query_db( query , data)
        return results


    @staticmethod
    def validate_comment(data):
        is_valid = True 
        if len(data['name']) < 2:
            flash(u"comment name must be at least 2 characters!", 'comment_error')
            is_valid = False
        if len(data['genre']) < 2:
            flash(u"Description must be at least 2 characters.", 'comment_error')
            is_valid = False
        if len(data['home_city']) < 2:
            flash(u"Home city must have at least 2 characters!", 'comment_error')
            is_valid = False
        if len(data['name']) > 255:
            flash(u"comment name can't be longer than 255 characters!", 'comment_error')
            is_valid = False
        if len(data['genre']) > 255:
            flash(u"Genre can't be longer than 255 characters.", 'comment_error')
            is_valid = False
        if len(data['home_city']) > 255:
            flash(u"Home city can't be longer than 255 characters.", 'comment_error')
            is_valid = False
            return is_valid
        if not is_valid:
            return is_valid

        if not GENRE_REGEX.match(data['genre']): 
            flash(u"The comment genre can only contain letters!", 'comment_error')
            is_valid = False
        return is_valid

from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Idea:
    def __init__( self , data ):
        self.id = data['id']
        self.idea_description = data['idea_description']
        self.title = data['title']
        self.idea_expanded = data['idea_expanded']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
# This is the section where the data of the user who made it is parsed in to extract name and id for session and display of the name of said user
        self.user_id = data['user_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.topic_id = data['topic_id']
        self.topic_name = data['topic_name']
# End of section

        self.liked_by = []
        self.comments = []

    @classmethod
    def get_ideas_with_users_and_topics( cls ):
        query = """
        SELECT * FROM ideas 
        LEFT JOIN users ON ideas.user_id = users.id
        LEFT JOIN topics ON ideas.topic_id = topics.id;"""
        results = connectToMySQL('bright_ideas').query_db( query )
        ideas = []
        for idea in results:
            ideas.append(cls(idea))
        return ideas

    @classmethod
    def get_likes_of_idea( cls, data ):
        query = """
        SELECT * FROM ideas_likes  
        LEFT JOIN users ON ideas_likes.user_id = users.id
        LEFT JOIN ideas ON ideas_likes.idea_id = ideas.id
        WHERE idea_id = %(id)s;"""
        results = connectToMySQL('bright_ideas').query_db( query , data )
        likes = []
        for like in results:
            data2 = {
                'id': like['id'],
                'first_name': like['first_name'],
                'last_name': like['last_name'],
                'email': like['email'],
                'password': like['password'],
                'updated_at': like['updated_at'],
                'created_at': like['created_at'],
            }
            likes.append(user.User(data2))
        return likes

    @classmethod
    def delete_like_of_idea( cls , data ):
        query = """
        DELETE FROM ideas_likes WHERE idea_id = %(idea_id)s AND user_id = %(user_id)s
        """
        results = connectToMySQL('bright_ideas').query_db( query , data)
        return results

    @classmethod
    def create_like_of_idea( cls , data ):
        query = """
        INSERT INTO ideas_likes (idea_id, user_id) VALUES (%(idea_id)s ,  %(user_id)s)
        """
        results = connectToMySQL('bright_ideas').query_db( query , data)
        return results

    @classmethod
    def get_one_idea_with_user( cls, data ):
        query = """
        SELECT * FROM ideas 
        JOIN users ON ideas.user_id = users.id
        JOIN topics ON ideas.topic_id = topics.id
        WHERE ideas.id = %(id)s;"""
        results = connectToMySQL('bright_ideas').query_db( query , data)
        idea = cls(results[0])
        return idea

    @classmethod
    def get_ideas_of_topic( cls, data ):
        query = """
        SELECT * FROM ideas 
        JOIN users ON ideas.user_id = users.id
        JOIN topics ON ideas.topic_id = topics.id
        WHERE topics.id = %(id)s;"""
        results = connectToMySQL('bright_ideas').query_db( query , data)
        idea = cls(results[0])
        return idea
        

    @classmethod
    def save_into_db(cls, data ):
        query = """
        INSERT INTO ideas ( idea_description , title , idea_expanded , user_id, topic_id ) 
        VALUES ( %(idea_description)s , %(title)s , %(idea_expanded)s , %(user_id)s, %(topic_id)s );"""
        result_id = connectToMySQL('bright_ideas').query_db( query, data )
        return result_id

    @classmethod
    def delete_idea(cls, data ):
        query = """
        DELETE FROM ideas WHERE id = %(id)s;"""
        result_is_none = connectToMySQL('bright_ideas').query_db( query, data )
        return result_is_none

    @classmethod
    def update_idea(cls, data ):
        query = """
        UPDATE ideas
        SET idea_description = %(idea_description)s, title = %(title)s, idea_expanded =  %(idea_expanded)s, updated_at = NOW()
        WHERE id = %(id)s;"""
        result_is_none = connectToMySQL('bright_ideas').query_db( query, data )
        return result_is_none

    @staticmethod
    def validate_idea(data):
        is_valid = True 
        if len(data['idea_description']) < 2:
            flash(u"Your idea must be at least 2 characters!", 'idea_error')
            is_valid = False
        if data['title']:
            if len(data['title']) < 2:
                flash(u"Title must be at least 2 characters.", 'idea_error')
                is_valid = False
            if len(data['title']) > 255:
                flash(u"Title can't be longer than 255 characters.", 'idea_error')
                is_valid = False
        if data['idea_expanded']:
            if len(data['idea_expanded']) < 2:
                flash(u"The expanded idea must have at least 2 characters!", 'idea_error')
                is_valid = False
        if len(data['idea_description']) > 255:
            flash(u"Your idea can't be longer than 255 characters!", 'idea_error')
            is_valid = False
        return is_valid

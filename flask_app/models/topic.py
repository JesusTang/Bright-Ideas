from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from flask_app.models import idea
import re

GENRE_REGEX = re.compile(r'^[a-zA-Z]') 

class Topic:
    def __init__( self , data ):
        self.id = data['id']
        self.topic_name = data['topic_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ideas = []

        self.liked_by = []

    @classmethod
    def get_all_topics( cls ):
        query = """
        SELECT * FROM topics;
        """
        results = connectToMySQL('bright_ideas').query_db( query )
        topics = []
        for topic in results:
            topics.append(cls(topic))
        return topics

    @classmethod
    def get_one_topic_with_ideas( cls, data ):
        query = """
        SELECT * FROM topics 
        LEFT JOIN ideas ON ideas.topic_id = topics.id
        LEFT JOIN users ON ideas.user_id = users.id
        WHERE topics.id = %(id)s;"""
        results = connectToMySQL('bright_ideas').query_db( query , data)
        topic = cls(results[0])
        for row in results:
            if not row['ideas.id']:
                return topic
            data1 = {
                'id': row['ideas.id'],
                'idea_description': row['idea_description'],
                'title': row['title'],
                'idea_expanded': row['idea_expanded'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'updated_at': row['updated_at'],
                'user_id' : row['user_id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'topic_id' : row['topic_id'],
                'topic_name': row['topic_name'],
            }
            topic.ideas.append(idea.Idea(data1))
        return topic
    

    @classmethod
    def get_topics_liked_by_user( cls , data):
        query = """
        SELECT * FROM topics_likes 
        LEFT JOIN topics ON topics_likes.topic_id = topics.id
        LEFT JOIN users ON topics_likes.user_id = users.id
        WHERE user_id = %(id)s;"""
        results = connectToMySQL('bright_ideas').query_db( query , data)
        topics = []
        if not results:
            return topics
        for row in results:
            topics.append(cls(row))
        return topics

    @classmethod
    def get_likes_of_topic( cls, data ):
        query = """
        SELECT * FROM topics_likes  
        LEFT JOIN users ON topics_likes.user_id = users.id
        LEFT JOIN topics ON topics_likes.topic_id = topics.id
        WHERE topic_id = %(id)s;"""
        results = connectToMySQL('bright_ideas').query_db( query , data )
        likes = []
        if not results:
            return likes
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
    def delete_like_of_topic( cls , data ):
        query = """
        DELETE FROM topics_likes WHERE topic_id = %(topic_id)s AND user_id = %(user_id)s
        """
        results = connectToMySQL('bright_ideas').query_db( query , data)
        return results

    @classmethod
    def create_like_of_topic( cls , data ):
        query = """
        INSERT INTO topics_likes (topic_id, user_id) VALUES (%(topic_id)s ,  %(user_id)s)
        """
        results = connectToMySQL('bright_ideas').query_db( query , data)
        return results
# CREATE ROUTES FOR THE TEMPLATE ONE_TOPIC_IDEAS.html

"""
    SELECT * FROM ideas_likes
    WHERE users.id = 1;
"""
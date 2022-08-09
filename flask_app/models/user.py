from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import idea
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.ideas = []
        self.comments = []

        self.ideas_liked = []
        self.comments_liked = []
        self.topics_liked = []

    @classmethod
    def get_all(cls):
        query = """SELECT * FROM users;"""
        results = connectToMySQL('bright_ideas').query_db(query)
        users = []
        for row_from_db in results:
            users.append( cls(row_from_db) )
        return users

    @classmethod
    def save_into_db(cls, data ):
        query = """
        INSERT INTO users ( first_name , last_name , email, password) 
        VALUES ( %(first_name)s , %(last_name)s , %(email)s, %(password)s);"""
        result_id = connectToMySQL('bright_ideas').query_db( query, data )
        return result_id

    @classmethod
    def get_by_email(cls, data ):
        query = """ 
        SELECT * FROM users 
        WHERE email = %(email)s;"""
        results = connectToMySQL('bright_ideas').query_db( query, data )
        if not results:
            return results
        user = cls(results[0])
        return user

    @classmethod
    def get_by_id(cls, data ):
        query = """ 
        SELECT * FROM users 
        WHERE id = %(id)s;"""
        results = connectToMySQL('bright_ideas').query_db( query, data )
        if not results:
            return results
        user = cls(results[0])
        return user

    @classmethod
    def get_user_with_ideas_liked(cls,data):
        query = """
        SELECT * FROM users 
        LEFT JOIN ideas_likes ON users.id = ideas_likes.user_id
        LEFT JOIN ideas ON ideas_likes.idea_id = ideas.id
        LEFT JOIN topics ON ideas.topic_id = topics.id
        LEFT JOIN users AS user_OWNER ON ideas.user_id = user_OWNER.id
        WHERE users.id = %(id)s;"""
        results = connectToMySQL('bright_ideas').query_db(query,data)
        user = cls(results[0])
        for row in results:
            if row['ideas.id'] == None:
                break
            data1 = {
                "id": row['ideas.id'],
                "idea_description": row['idea_description'],
                "title": row['title'],
                "idea_expanded": row['idea_expanded'],
                "created_at": row['ideas.created_at'],
                "updated_at": row['ideas.updated_at'],
                # This is the section where the data of the user who made it is parsed in to extract name and id for session and display of the name of said user
                "user_id": row['user_OWNER.id'],
                'first_name' : row['user_OWNER.first_name'],
                'last_name' : row['user_OWNER.last_name'],
                'topic_name' : row['topic_name'],
                'topic_id' : row['topic_id'],
                # End of section
            }
            user.ideas_liked.append(idea.Idea(data1)) 
        return user

    @classmethod
    def get_user_owned_ideas(cls,data):
        query = """
        SELECT * FROM users 
        LEFT JOIN ideas ON ideas.user_id = users.id
        LEFT JOIN topics ON ideas.topic_id = topics.id
        WHERE users.id = %(id)s;"""
        results = connectToMySQL('bright_ideas').query_db(query,data)
        user = cls(results[0])
        for row in results:
            if row['ideas.id'] == None:
                break
            data1 = {
                "id": row['ideas.id'],
                "idea_description": row['idea_description'],
                "title": row['title'],
                "idea_expanded": row['idea_expanded'],
                "created_at": row['ideas.created_at'],
                "updated_at": row['ideas.updated_at'],
                # This is the section where the data of the user who made it is parsed in to extract name and id for session and display of the name of said user
                "user_id": row['user_id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'topic_name' : row['topic_name'],
                'topic_id' : row['topic_id'],
                # End of section
            }
            user.ideas.append(idea.Idea(data1)) 
        return user


    @classmethod
    def add_member(cls,data):
        query = "INSERT INTO idea_members (user_id,idea_id) VALUES (%(user_id)s,%(idea_id)s);"
        return connectToMySQL('bright_ideas').query_db(query,data)

    @classmethod
    def remove_member(cls,data):
        query = "DELETE FROM idea_members WHERE user_id =%(user_id)s AND idea_id = %(idea_id)s;"
        return connectToMySQL('bright_ideas').query_db(query,data)

    @staticmethod
    def validate_user_for_registration(data):
        is_valid = True 
        if len(data['first_name']) < 2:
            flash(u"First name must be at least 2 characters.", 'registration_error')
            is_valid = False
        if len(data['last_name']) < 2:
            flash(u"Last name must be at least 2 characters.", 'registration_error')
            is_valid = False
        if len(data['email']) < 1:
            flash(u"Email can't be left blank!.", 'registration_error')
            is_valid = False
        if len(data['password']) < 8:
            flash(u"Password must be at least 8 characters.", 'registration_error')
            is_valid = False
        if is_valid == False:
            return is_valid

        if not EMAIL_REGEX.match(data['email']): 
            flash(u"Invalid email address!", 'registration_error')
            is_valid = False

        if not data['password'] == data['confirm_password']:
            flash(u"Passwords must match.", 'registration_error')
            is_valid = False
        if (User.get_by_email(data)):
            flash("This email already exists!", 'registration_error')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_user_for_login(data):
        is_valid = True
        if not data['email']:
            flash(u"Email can't be left blank!", 'login_error')
            is_valid = False
        if not data['password']:
            flash(u"Password can't be left blank!", 'login_error')
            is_valid = False
            return is_valid
        if not User.get_by_email(data):
            flash(u"Email doesn't exist!", 'login_error')
            is_valid = False
            return is_valid
        return is_valid
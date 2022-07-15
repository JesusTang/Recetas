from turtle import isvisible
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
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

        self.recipes = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('recetas').query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def save_into_db(cls, data ):
        query = """
        INSERT INTO users ( first_name , last_name , email, password) 
        VALUES ( %(first_name)s , %(last_name)s , %(email)s, %(password)s);"""
        result_id = connectToMySQL('recetas').query_db( query, data )
        return result_id

    @classmethod
    def get_by_id(cls, data ):
        query = """
        SELECT * FROM users 
        WHERE id = %(id)s;"""
        results = connectToMySQL('recetas').query_db( query, data )
        users = []
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def get_by_email(cls, data ):
        query = """ 
        SELECT * FROM users 
        WHERE email = %(email)s;"""
        results = connectToMySQL('recetas').query_db( query, data )
        users = []
        for user in results:
            users.append( cls(user) )
        return users


    @staticmethod
    def validate_user_for_registration(data):
        is_valid = True 
        if len(data['first_name']) < 2:
            flash(u"First name must be at least 2 characters.", 'registration_error')
            is_valid = False
        if len(data['last_name']) < 2:
            flash(u"Last name must be at least 2 characters.", 'registration_error')
            is_valid = False

        if (User.get_by_email(data)):
            flash("This email already exists!", 'registration_error')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash(u"Invalid email address!", 'registration_error')
            is_valid = False

        if len(data['password']) < 8:
            flash(u"Password must be at least 8 characters.", 'registration_error')
            is_valid = False
        if not data['password'] == data['confirm_password']:
            flash(u"Passwords must match.", 'registration_error')
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
        if not str(data['password']) == str((User.get_by_email(data))[0].password):
            flash(u"Password is incorrect", 'login_error')
            is_valid = False
            return is_valid
        return is_valid
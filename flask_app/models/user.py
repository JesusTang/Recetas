from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import recipe
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

        self.recipes_liked = []

    @classmethod
    def get_all(cls):
        query = """SELECT * FROM users
        JOIN recipes ON users.recipe_id = recipes.id;"""
        results = connectToMySQL('recetas').query_db(query)
        users = []
        for row_from_db in results:
            users.append( cls(row_from_db) )

# This section is optional
            for user in users:
                recipe_data = {
                    "id" : row_from_db["recipe.id"],
                    "name" : row_from_db["name"],
                    "instructions" : row_from_db["instructions"],
                    "description" : row_from_db["description"],
                    "date_cooked_at" : row_from_db["date_cooked_at"],
                    "under_30" : row_from_db["under_30"],
                    "created_at" : row_from_db["recipe.created_at"],
                    "updated_at" : row_from_db["recipe.updated_at"],
                    "users_liked" : row_from_db["users_liked"],
                    # This is the section where the data of the user who made it is parsed in to extract name and id for session and display of the name of said user
                    'first_name' : row_from_db['first_name'],
                    'last_name' : row_from_db['last_name'],
                    'user_id' : row_from_db['user_id']
                    # End of section
                }
                user.recipes.append( recipe.Recipe( recipe_data ) )
# End of section

        return users

    @classmethod
    def save_into_db(cls, data ):
        query = """
        INSERT INTO users ( first_name , last_name , email, password) 
        VALUES ( %(first_name)s , %(last_name)s , %(email)s, %(password)s);"""
        result_id = connectToMySQL('recetas').query_db( query, data )
        return result_id

    @classmethod
    def get_by_email(cls, data ):
        query = """ 
        SELECT * FROM users 
        WHERE email = %(email)s;"""
        results = connectToMySQL('recetas').query_db( query, data )
        user = cls(results[0])
        return user

    @classmethod
    def get_by_id(cls,data):
        query = """
        SELECT * FROM users 
        LEFT JOIN likes ON users.id = likes.user_id 
        LEFT JOIN recipes ON recipes.id = likes.recipe_id 
        WHERE users.id = %(id)s;"""
        results = connectToMySQL('recetas').query_db(query,data)
        user = cls(results[0])
        for row in results:
            if row['recipes.id'] == None:
                break
            data = {
                "id": row['recipes.id'],
                "name": row['name'],
                "description": row['description'],
                "instructions": row['instructions'],
                "date_cooked_at": row['date_cooked_at'],
                "under_30": row['under_30'],
                "created_at": row['recipes.created_at'],
                "updated_at": row['recipes.updated_at'],
                # This is the section where the data of the user who made it is parsed in to extract name and id for session and display of the name of said user
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'user_id' : row['user_id']
                # End of section
            }
            user.recipes_liked.append(recipe.Recipe(data))
        return user

    @classmethod
    def add_like(cls,data):
        query = "INSERT INTO likes (user_id,recipe_id) VALUES (%(user_id)s,%(recipe_id)s);"
        return connectToMySQL('recetas').query_db(query,data)

    @classmethod
    def remove_like(cls,data):
        query = "DELETE FROM likes WHERE user_id =%(user_id)s AND recipe_id = %(recipe_id)s;"
        return connectToMySQL('recetas').query_db(query,data)

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
        return is_valid
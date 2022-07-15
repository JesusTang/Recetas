from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

NAME_REGEX = re.compile(r'^[a-zA-Z]') 

class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked_at = data['date_cooked_at']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_recipes_with_users( cls ):
        query = """
        SELECT * FROM recipes 
        JOIN users ON recipes.user_id = users.id;"""
        results_dict = connectToMySQL('recetas').query_db( query )
        return results_dict

    @classmethod
    def save_into_db(cls, data ):
        query = """
        INSERT INTO recipes ( name , description , instructions , date_cooked_at , under_30, user_id ) 
        VALUES ( %(name)s , %(description)s , %(instructions)s , %(date_cooked_at)s , %(under_30)s, %(user_id)s );"""
        result_id = connectToMySQL('recetas').query_db( query, data )
        return result_id

    @classmethod
    def delete_recipe(cls, data ):
        query = """
        DELETE FROM recipes WHERE id = %(id)s;"""
        result_is_none = connectToMySQL('recetas').query_db( query, data )
        return result_is_none

    @classmethod
    def update_recipe(cls, data ):
        query = """
        UPDATE recipes
        SET name = %(name)s, description = %(description)s, instructions =  %(instructions)s, date_cooked_at =  %(date_cooked_at)s, under_30 =  %(under_30)s, updated_at = NOW()
        WHERE id = %(id)s;"""
        result_is_none = connectToMySQL('recetas').query_db( query, data )
        return result_is_none

    @classmethod
    def get_recipe_with_users_by_id(cls, data ):
        query = """
        SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"""
        result_dict = connectToMySQL('recetas').query_db( query, data )
        return result_dict


    @staticmethod
    def validate_recipe(data):
        is_valid = True 
        if len(data['name']) < 3:
            flash(u"Recipe name must be at least 3 characters!", 'recipe_error')
            is_valid = False
        if len(data['description']) < 3:
            flash(u"Description must be at least 3 characters.", 'recipe_error')
            is_valid = False
        if len(data['instructions']) < 3:
            flash(u"Instructions can't be longer than 255 characters!", 'recipe_error')
            is_valid = False
        if not data['date_cooked_at']:
            flash(u"Date can't be left blank!", 'recipe_error')
            is_valid = False
        if len(data['name']) > 255:
            flash(u"Recipe name can't be longer than 255 characters!", 'recipe_error')
            is_valid = False
        if len(data['description']) > 255:
            flash(u"Description can't be longer than 255 characters.", 'recipe_error')
            is_valid = False
        if len(data['instructions']) > 255:
            flash(u"Instructions can't be longer than 255 characters.", 'recipe_error')
            is_valid = False
            return is_valid
        if not is_valid:
            return is_valid

        if not NAME_REGEX.match(data['name']): 
            flash(u"The recipe name can only contain letters!", 'recipe_error')
            is_valid = False
        return is_valid

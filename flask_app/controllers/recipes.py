from flask_app import app
from flask import render_template,redirect,request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.recipe import Recipe 
from flask_app.models.user import User
bcrypt = Bcrypt(app)


@app.route("/recipes")
def show_all_recipes():
    recipes = Recipe.get_recipes_with_users()
    if not session:
        flash(u"There's no user logged in!", "general_error")
        return redirect('/')
    data = {
        'id' : session['id']}
    user = User.get_by_id(data)
    id_of_recipes_liked = []
    for recipe in user.recipes_liked:
        id_of_recipes_liked.append(recipe.id)
    return render_template('recipes_of_everyone.html', recipes = recipes, user = user, list_of_recipes_liked = id_of_recipes_liked)

@app.route("/recipes/new")
def add_new_recipe():
    if not session:
        flash(u"There's no user logged in!", "general_error")
        return redirect('/')
    return render_template('add_recipe.html')

@app.route('/process-new-recipe', methods=['POST'])
def process_new_recipe():
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_cooked_at': request.form['date_cooked_at'],
        'under_30': request.form['under_30'],
        'user_id': session['id']
    }
    if not Recipe.validate_recipe(data):
        return redirect('/recipes/new')
    Recipe.save_into_db(data)
    return redirect('/recipes')


@app.route('/recipes/<recipe_id>')
def show_one_recipe(recipe_id):
    if not session:
        flash(u"There's no user logged in!", "general_error")
        return redirect('/')
    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_one_recipe_with_user(data)
    number_of_likes = len(recipe.users_liked)
    return render_template('recipe_description.html', recipe = recipe, number_of_likes = number_of_likes)

@app.route('/recipes/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    if not session:
        flash(u"There's no user logged in!", "general_error")
        return redirect('/')
    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_one_recipe_with_user(data)
    if session['id'] != recipe.user_id:
        return redirect('/recipes')
    return render_template('edit_recipe.html', recipe = recipe)

@app.route('/process-edit-recipe-<recipe_id>', methods=['POST'])
def process_edit_recipe(recipe_id):
    id = recipe_id
    data = {
        'id' : recipe_id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_cooked_at': request.form['date_cooked_at'],
        'under_30': request.form['under_30'],
    }
    if not Recipe.validate_recipe(data):
        return redirect(f'/recipes/edit/{id}')
    Recipe.update_recipe(data)
    return redirect('/recipes')

@app.route('/delete-recipe-<int:recipe_id>')
def processing_delete_recipe(recipe_id):
    data = {
        'id': recipe_id
    }
    Recipe.delete_recipe(data)
    return redirect('/recipes')

# @app.route('')

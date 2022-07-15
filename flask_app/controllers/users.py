from flask_app import app
from flask import render_template,redirect,request, flash, session
from flask_app.models.recipe import Recipe 
from flask_app.models.user import User

@app.route("/")
def log_and_reg():
    return render_template("register_and_login.html")

@app.route("/process-register", methods=['POST'])
def process_register():
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirm_password': request.form['confirm_password']
    }
    if not User.validate_user_for_registration(data):
        return redirect('/')
    id = User.save_into_db(data)
    print(id)
    data = {
        'id': id
    }
    user = User.get_by_id(data)
    print(user)
    session['id'] = user[0].id
    session['first_name'] = user[0].first_name
    session['last_name'] = user[0].last_name
    return redirect("/recipes")

@app.route("/process-login", methods=['POST'])
def process_login():
    data = {
        'email': request.form['email'],
        'password': request.form['password']
    }
    if not User.validate_user_for_login(data):
        return redirect('/')
    user = User.get_by_email(data)
    print(user)
    session['id'] = user[0].id
    session['first_name'] = user[0].first_name
    session['last_name'] = user[0].last_name
    return redirect('/recipes')

@app.route("/recipes")
def show_all_recipes():
    recipes = Recipe.get_recipes_with_users()
    if not session:
        flash(u"There's no user logged in!", "general_error")
        return redirect('/')
    return render_template('recipes_of_everyone.html', recipes = recipes)

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
    print('YOU SHOULD BE LOOKING AT THIS')
    print(request.form)
    print(data)
    if not Recipe.validate_recipe(data):
        return redirect('/recipes/new')
    Recipe.save_into_db(data)
    return redirect('/recipes')

@app.route('/process-logout')
def process_logout():
    session.clear()
    return redirect('/')

@app.route('/recipes/<recipe_id>')
def show_one_recipe(recipe_id):
    if not session:
        flash(u"There's no user logged in!", "general_error")
        return redirect('/')
    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_recipe_with_users_by_id(data)
    return render_template('recipe_description.html', recipe = recipe[0])

@app.route('/recipes/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    if not session:
        flash(u"There's no user logged in!", "general_error")
        return redirect('/')
    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_recipe_with_users_by_id(data)
    return render_template('edit_recipe.html', recipe = recipe[0])

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

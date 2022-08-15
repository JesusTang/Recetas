from flask_app import app
from flask import render_template,redirect,request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
bcrypt = Bcrypt(app)


@app.route("/")
def log_and_reg():
    return render_template("register_and_login.html")

@app.route("/process-register", methods=['POST'])
def process_register():
    if not User.validate_user_for_registration(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    confirm_pw_hash = bcrypt.generate_password_hash(request.form['confirm_password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash,
        'confirm_password': confirm_pw_hash
    }
    id = User.save_into_db(data)
    data = {
        'id': id
    }
    user = User.get_by_id(data)
    session['id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    return redirect("/recipes")

@app.route("/process-login", methods=['POST'])
def process_login():
    data = {
        'email': request.form['email'],
        'password': request.form['password']
    }
    user_in_db = User.get_by_email(data)
    if not User.validate_user_for_login(data):
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash(u"Invalid password", 'login_error')
        return redirect('/')
    user = User.get_by_email(data)
    session['id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    return redirect('/recipes')

@app.route("/add-like-<int:recipe_id>")
def add_a_like(recipe_id):
    data = {
        'user_id' : session['id'],
        'recipe_id': recipe_id
    }
    User.add_like(data)
    return redirect('/recipes')

@app.route("/remove-like-<int:recipe_id>")
def remove_a_like(recipe_id):
    data = {
        'user_id' : session['id'],
        'recipe_id': recipe_id
    }
    User.remove_like(data)
    return redirect('/recipes')

@app.route('/process-logout')
def process_logout():
    session.clear()
    return redirect('/')

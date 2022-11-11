from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
# another model
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


# '/' GET
@app.route('/')
def index():
    return render_template('index.html')


# '/register' POST
@app.route('/register', methods=['POST'])
def register():
    if not User.valid_user(request.form):
        flash('Invalid Email/Password')
        return redirect('/')
    data = {
        "f_name" : request.form['f_name'],
        "l_name" : request.form['l_name'],
        "email" : request.form['email'],
        "password" : bcrypt.generate_password_hash(request.form['password'])
    }
    session['user_id'] = User.create(data)
    return redirect('/dashboard')


# '/login' POST
@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email({"email" : request.form['email']})
    if user:
        if bcrypt.check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            return redirect('/dashboard')
    flash('Invalid Email/Password')
    return redirect('/')


# '/logout'
@app.route('/logout')
def logout():
    session.pop('user_id')
    # or session.clear() if there's a preference
    return redirect('/')


# '/dashboard' => INCOMPLETE ROUTE (populate posts for dashboard)
@app.route('/dashboard')
def dashboard():
    if "user_id" in session:
        return render_template('dashboard.html', user=User.get_by_id({"id" : session['user_id']}))


# PROFILE PAGE - find user by id => INCOMPLETE ROUTE (populate user's own posts)
@app.route('/user/<int:id>')
def profile(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : id
    }
    user_data = {
        "id" : session['user_id']
    }
    return render_template('profile.html', user=User.get_by_id(user_data))
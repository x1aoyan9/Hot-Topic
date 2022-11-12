from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.topics import Topic
from flask_app.models.comments import Comment
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
# Fallon - added all_topics
@app.route('/dashboard')
def dashboard():
    if "user_id" in session:
        return render_template('dashboard.html', user=User.get_by_id({"id" : session['user_id']}), all_topics=Topic.get_topics_with_creator())


# PROFILE PAGE - find user by id => INCOMPLETE ROUTE (populate user's own posts)
#Fallon - added topics belonging to user (I used user_data as that is what user variable is using)
@app.route('/user/<int:id>')
def profile(id):
    if 'user_id' not in session:
        return redirect('/logout')
    #Fallon - not sure what the below data is for, its unused, and if you are setting user variable to the session user, then is there a need for another user id? Is the profile only viewable if its yours? If yes then we dont need the current data, if no then we dont need the session user_id data
    data = {
        "id" : id
    }
    user_data = {
        "id" : session['user_id']
    }
    return render_template('profile.html', user=User.get_by_id(user_data), topics=Topic.get_topics_by_user(user_data))

#Navigate to the create a topic page
@app.route('/create', methods=['GET'])
def create_page():
    if not session:
        flash('Please log in first!')
        return redirect('/')
    return render_template('createForm.html')

#CreateForm submission route for new topic
@app.route('/create/submit', methods=['POST'])
def create_topic():
    data = {
        'title' : request.form['title'],
        'question' : request.form['question'],
        'choice1' : request.form['choice1'],
        'choice2' : request.form['choice2'],
        'choice3' : request.form['choice3'],
        'choice4' : request.form['choice4'],
        'choice5' : request.form['choice5'],
        'user_id' : session['user_id']
    }
    if not Topic.validate_topic(data):
        return redirect('/create')
    Topic.create_topic(data)
    return redirect('/dashboard')

#View the topic in a separate page, INCOMPLETE needs the actual html page made for the actual vote functionality
@app.route('/view_topic/<int:topic_id>', methods=['get'])
def view_topic(topic_id):
    data = {
        'id': topic_id
        }
    return render_template('INSERT VIEW/VOTE HTML', topic=Topic.get_one_topic(data))
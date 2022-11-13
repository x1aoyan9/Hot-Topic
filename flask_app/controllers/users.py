from flask_app import app
from flask import render_template, redirect, request, session, flash, get_flashed_messages
from flask_app.models.user import User
from flask_app.models.topic import Topic
from flask_app.models.comment import Comment
from flask_app.models.response import Response
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
    session['user_id'] = User.create_user(data)
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
    return redirect('/')


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
    return render_template('profile.html', user=User.get_by_id(data), topics=Topic.get_topics_by_user(data))

# @app.route('/user/<int:id>/edit', methods = ['get'])
# def edit_profile(id):
#     if 'user_id' not in session:
#         return redirect('/logout')
#     return render_template('edit_profile.html', user = User.get_by_id({'id': id}), messages = get_flashed_messages())

#Navigate to the create a topic page
@app.route('/create', methods=['GET'])
def create_page():
    if not session:
        flash('Please log in first!')
        return redirect('/')
    return render_template('createForm.html', user = User.get_by_id({'id': session['user_id']}), messages = get_flashed_messages())

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
    if not Response.validate_vote(data):
        flash('Cannot vote twice! View results to view the topic instead.', 'attempt_vote')
        return redirect('/dashboard')
    return render_template('viewTopic.html', topic=Topic.get_one_topic(data))

#vote/choice sumbission from form on the view topic page, incomplete needs a results view page built as well
@app.route('/view_topic/submit_choice/<int:topic_id>', methods=['post'])
def submit_choice(topic_id):
    data = {
        'choice' : request.form['choice'],
        'user_id' : session['user_id'],
        'topic_id' : topic_id
    }
    Response.submit_choice(data)
    return redirect('/results/' + str(topic_id))

@app.route('/view_topic/<int:topic_id>/edit', methods=['get'])
def edit_page(topic_id):
    data = {'id':topic_id}
    return render_template('updateForm.html', topic=Topic.get_one_topic(data), messages = get_flashed_messages(), user = User.get_by_id({'id': session['user_id']}))

@app.route('/view_topic/<int:topic_id>/edit', methods=['post'])
def edit_submit(topic_id):
    print(request.form)
    data={
        'id' : topic_id,
        'title' : request.form['title'],
        'question' : request.form['question'],
        'choice1' : request.form['choice1'],
        'choice2' : request.form['choice2'],
        'choice3' : request.form['choice3'],
        'choice4' : request.form['choice4'],
        'choice5' : request.form['choice5']
    }
    if not Topic.validate_topic(data):
        return redirect(request.referrer)
    Topic.update_topic(data)
    return redirect('/view_topic/' + str(topic_id))

@app.route('/view_topic/<int:topic_id>/delete', methods=['get'])
def delete_topic(topic_id):
    data = {
        'id' : topic_id
    }
    Topic.delete_topic(data)
    return redirect('/dashboard')

#results view page, needs the html document
@app.route('/results/<int:topic_id>', methods=['get'])
def view_results(topic_id):
    data = {
        'id' : topic_id
    }
    return render_template('results.html', topic=Topic.get_one_topic(data), all_responses=Topic.get_all_responses(data), all_comments=Comment.get_comments(data), choice1_total=Topic.get_choice1_total(data), choice2_total=Topic.get_choice2_total(data), choice3_total=Topic.get_choice3_total(data), choice4_total=Topic.get_choice4_total(data), choice5_total=Topic.get_choice5_total(data), user = User.get_by_id({'id': session['user_id']}), all_users = User.get_all_users())

#Comment submission, should just refresh the page and add the comment to the all_comments array
@app.route('/results/<int:topic_id>/comment', methods = ['post'])
def submit_comment(topic_id):
    data = {
        'comment' : request.form['comment'],
        'user_id' : session['user_id'],
        'topic_id' : topic_id
    }
    Comment.add_comment(data)
    return redirect(request.referrer)

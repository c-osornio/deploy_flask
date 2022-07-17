from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import user, magazine

# Create
@app.route('/users/register', methods=['POST'])
def register_user():
    if user.User.save(request.form):
        return redirect(f'/users/profile/{session["user_id"]}')
    return render_template('index.html', info = request.form)

# Read
@app.route('/')
def index():
    return render_template('index.html', info = request.form)

@app.route('/users/profile/<int:id>')
def show_profile(id):
    if 'user_id' not in session:
        return redirect('/')
    return render_template('profile.html', user = user.User.get_user_by_id(id), all_magazines = magazine.Magazine.get_all())

@app.route('/users/<int:id>/edit')
def show_account_form(id):
    return render_template('edit_account.html', user = user.User.get_user_by_id(id), all_magazines = magazine.Magazine.get_all())

# Update
@app.route('/users/<int:id>/update', methods=['POST'])
def update_user(id):
    if user.User.validate_user_edit_data(request.form): 
        user.User.update(request.form)
        return redirect(f'/users/profile/{session["user_id"]}')
    return redirect(f'/users/{id}/edit')


# Destroy

# Login
@app.route('/users/login', methods=['POST'])
def login():
    if user.User.login(request.form):
        return redirect(f'/users/profile/{session["user_id"]}')
    return render_template('index.html',info = request.form)

# Logout
@app.route('/users/logout')
def logout():
    session.clear()
    return redirect('/')
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import user, magazine

# Create
@app.route('/magazine/create_new', methods=['POST'])
def create_magazine():
    if "user_id" in session:
        if magazine.Magazine.save(request.form):
            return redirect(f'/users/profile/{session["user_id"]}')
        return render_template('create_magazine.html', info = request.form)
    return redirect('/')

# Read
@app.route('/magazines/create')
def show_create_magazine_form():
    if "user_id" in session:
        return render_template('create_magazine.html', info = request.form)
    return redirect('/')

@app.route('/magazines/<int:id>')
def show_magazine(id):
    if "user_id" in session:
        return render_template('show_magazine.html', magazine = magazine.Magazine.getOne(id))
    return redirect('/')

@app.route('/magazines/<int:id>/subscribe', methods=['POST'])
def subscribe(id):
    magazine.Magazine.subscribe(request.form)
    return redirect(f'/users/profile/{session["user_id"]}')

#Delete
@app.route('/magazines/<int:id>/delete')
def delete_magazine(id):
    magazine.Magazine.delete(id)
    return redirect(f'/users/{session["user_id"]}/edit')
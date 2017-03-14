"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import db, app
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, FileField, RadioField, SubmitField
from wtforms.validators import DataRequired
from random import randint
import os
import datetime
from app.models import UserProfile

class MyForm(FlaskForm):
    fname = TextField('First Name', validators=[DataRequired()])
    lname = TextField('Last Name', validators=[DataRequired()])
    username = TextField('Username', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    biography = TextAreaField('Biography', validators=[DataRequired()])
    image = FileField('Image', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('m','Male'), ('f','Female')])
    save = SubmitField("Add Profile")


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/profile', methods=['GET','POST'])
def profile():
    form = MyForm()
    
    if request.method == "POST":
        file_folder = app.config['UPLOAD_FOLDER']
        
        if form.validate_on_submit():
            fname = request.form['fname']
            lname = request.form['lname']
            username = request.form['username']
            age = request.form['age']
            biography = request.form['biography']
            gender = request.form['gender']
            image = request.files['image']
            
            imagename = secure_filename(image.filename)
            image.save(os.path.join(file_folder, imagename))
            
            userid = randint(100000, 999999)
            created_on = datetime.date.today()
            
            new_profile = UserProfile(userid, fname, lname, username, age, gender, biography, imagename, created_on)
            db.session.add(new_profile)
            db.session.commit()
            
            flash("Created Successfully", "success")
            return redirect(url_for("profile"))
    """Render the website's profile_form page."""
    return render_template('profile_form.html', form=form)


@app.route('/profiles', methods=['GET', 'POST'])
def profiles():
    user_profiles = db.session.query(UserProfile).all()
    
    if request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
        users = [{"username": user.username, "userid": user.userid} for user in user_profiles]
        return jsonify(users)
    """Render"""
    return render_template('profiles.html', users=user_profiles)
    
@app.route('/profile/<userid>', methods=['GET', 'POST'])
def profile_indi(userid):
    user = UserProfile.query.filter_by(userid=userid).first()
    if user is not None:
        if request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
            return jsonify(userid=user.userid, username=user.username, image=user.image, fname=user.fname, lname=user.lname, gender=user.gender, age=user.age, created_on=user.created_on )
        else:
            # Render user's profile page
            return render_template('view_profile.html', user=user)
    """Render"""
    return render_template('profile_form.html')
###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
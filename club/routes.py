from club import app
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request

@app.context_processor
def inject_globals():
    return {'current_year':datetime.now().year}
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/teams')
def teams():
    return render_template('teams.html')

@app.route('/fixtures')
def fixtures():
    return render_template('fixtures.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
from club import app
from datetime import datetime
from flask import render_template

@app.context_processor
def inject_globals():
    return {'current_year':datetime.now().year}
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

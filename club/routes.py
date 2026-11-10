from club import app
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, abort
from .models import (get_players, get_members, get_tournaments, get_tournament,
                      get_tournament_teams, get_tournament_matches)

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

@app.route('/team')
def team():
    members=get_members()
    players=get_players()
    return render_template('team.html', players=players, members=members)

@app.route('/tournament')
def tournament():
    tournaments=get_tournaments()
    return render_template('tournament/index.html', tournaments=tournaments)

@app.route('/tournament_details/<int:tournament_id>')
def tournament_details(tournament_id):
    tournament=get_tournament(tournament_id)
    if tournament is None:
        abort(404)
    teams=get_tournament_teams(tournament_id)
    matches=get_tournament_matches(tournament_id)
    fixtures=[]
    result=[]
    for match in matches:
        if match['status']=="completed":
          result.append(match)
        else:
            fixtures.append(match)
    return render_template('tournament/details.html',
                           tournament=tournament,
                           teams=teams,
                           fixtures=fixtures,
                           results=result)


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/register_page')
def register_page():
    return render_template('register.html')
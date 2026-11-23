from club import app
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, abort
from .models import (get_players, get_members, get_tournaments, get_tournament,
                      get_tournament_teams, get_tournament_matches,
                      get_match, get_match_events, add_match_event, delete_match_event,
                      get_tournament_team, get_team_players, add_team_player, delete_team_player)

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


@app.route('/match_stats/<int:match_id>')
def match_stats(match_id):
    match = get_match(match_id)
    if match is None:
        abort(404)

    events = get_match_events(match_id)

    # Separate goals and cards
    goals = [e for e in events if e.get('event_type') == 'goal']
    cards = [e for e in events if e.get('event_type') in ('green_card', 'yellow_card', 'red_card')]

    # Separate events by team for side-by-side match breakdown
    team1_goals = [e for e in goals if e.get('team_id') == match['team1_id']]
    team2_goals = [e for e in goals if e.get('team_id') == match['team2_id']]
    team1_cards = [e for e in cards if e.get('team_id') == match['team1_id']]
    team2_cards = [e for e in cards if e.get('team_id') == match['team2_id']]

    return render_template(
        'tournament/match_stats.html',
        match=match,
        events=events,
        goals=goals,
        cards=cards,
        team1_goals=team1_goals,
        team2_goals=team2_goals,
        team1_cards=team1_cards,
        team2_cards=team2_cards
    )


@app.route('/match_stats/<int:match_id>/add_event', methods=['POST'])
def add_match_event_route(match_id):
    team_id = request.form.get('team_id', type=int)
    player_name = request.form.get('player_name', '').strip()
    event_type = request.form.get('event_type', '').strip()

    if team_id and player_name and event_type in ('goal', 'green_card', 'yellow_card', 'red_card'):
        add_match_event(match_id, team_id, player_name, event_type)

    return redirect(url_for('match_stats', match_id=match_id))


@app.route('/match_stats/<int:match_id>/delete_event/<int:event_id>', methods=['POST'])
def delete_match_event_route(match_id, event_id):
    delete_match_event(event_id, match_id)
    return redirect(url_for('match_stats', match_id=match_id))


@app.route('/tournament_team/<int:team_id>')
def tournament_team_players(team_id):
    team = get_tournament_team(team_id)
    if team is None:
        abort(404)
    players = get_team_players(team_id)
    return render_template('tournament/team_players.html', team=team, players=players)


@app.route('/tournament_team/<int:team_id>/add_player', methods=['POST'])
def add_team_player_route(team_id):
    player_name = request.form.get('player_name', '').strip()
    jersey_number = request.form.get('jersey_number', type=int)
    position = request.form.get('position', '').strip()

    if player_name:
        add_team_player(team_id, player_name, jersey_number, position)

    return redirect(url_for('tournament_team_players', team_id=team_id))


@app.route('/tournament_team/<int:team_id>/delete_player/<int:player_id>', methods=['POST'])
def delete_team_player_route(team_id, player_id):
    delete_team_player(player_id, team_id)
    return redirect(url_for('tournament_team_players', team_id=team_id))




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
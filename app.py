from flask import Flask, request, jsonify
# from apis import match_summary, match_won_by_team, matches_by_venue, teams, player_of_match_performance,
import apis

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>IPL APIs<h1>'

@app.route('/teams')
def get_teams():
    return jsonify(apis.teams())
    
@app.route('/match_summary')
def get_match_summary():
    match_id = request.args.get('match_id')
    return jsonify(apis.match_summary(int(match_id)))

@app.route('/match_won_by_team')
def get_match_won_by_team():
    team = request.args.get('team')
    return jsonify(apis.match_won_by_team(team))

@app.route('/matches_by_venue')
def get_matches_by_venue():
    venue = request.args.get('venue')
    return jsonify(apis.matches_by_venue(venue)) 

@app.route('/player_of_match_performance')
def get_player_of_match_performance():
    player = request.args.get('player')
    return jsonify(apis.player_of_match_performance(player))

@app.route('/toss_decision_analysis')
def get_toss_decision_analysis():
    return jsonify(apis.toss_decision_analysis())

@app.route('/head_to_head')
def get_head_to_head():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    return jsonify(apis.head_to_head(team1, team2))

@app.route('/matches_by_margin')
def get_match_win_by_margin():
    margin_type = request.args.get('margin_type') # 'Runs' or 'Wickets'
    margin = request.args.get('margin')
    return jsonify(apis.matches_by_margin(margin_type,float(margin)))

@app.route('/player_matches')
def get_player_match():
    player = request.args.get('player')
    return jsonify(apis.player_matches(player))

@app.route('/season_analysis')
def get_matches_by_season():
    season = request.args.get('season')
    return jsonify(apis.matches_by_season(season))

@app.route('/super_over_matches')
def get_super_over_matches():
    return jsonify(apis.super_over_matches())

@app.route('/highest_margin_matches')
def get_highest_margin_matches():
    return jsonify(apis.highest_margin_matches())

@app.route('/season_summary')
def get_season_summary():
    season = request.args.get('season')
    return jsonify(apis.season_summary(season))

@app.route('/team_performance_over_seasons')
def get_team_performance_over_seasons():
    team = request.args.get('team')
    return jsonify(apis.team_performance_over_seasons(team))

@app.route('/player_career_summary')
def get_player_career_summary():
    player = request.args.get('player')
    return jsonify(apis.player_career_summary(player))

app.run(debug=True)
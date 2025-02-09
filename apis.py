import pandas as pd
import ast
df = pd.read_csv('IPL_dataset_cleaned.csv',index_col = 'ID')

# Convert string to list
for idx, match in df.iterrows():
    if isinstance(match['Team1Players'], str):
        df.at[idx, 'Team1Players'] = ast.literal_eval(match['Team1Players'])
    if isinstance(match['Team2Players'], str):
        df.at[idx, 'Team2Players'] = ast.literal_eval(match['Team2Players'])

# Function to get all teams
def teams():
    return {'teams' : list(set(list(df['Team1'])+list(df['Team2'])))}

# Function to get match summary
def match_summary(ID):
    try:
        x = df.loc[[ID]]
        return {'sumamry':x.to_dict()}
    except Exception as e:
        return {"error": "Match not found"}

# function to get match won by team
def match_won_by_team(team):
    matches = []
    for index,match in df.iterrows():
        if match['WinningTeam'] == team:
            matches.append({
                'Id' : index,
                'Against' : match['Team1'] if team==match['Team2'] else match['Team2'], 
                'Venue' : match['Venue'],
                'TossWinner' : match['TossWinner'],   
                'TossDecision' : match['TossDecision'],
                'SuperOver' : 'No' if match['SuperOver']=='N' else 'Yes',
                'WonBy' : match['WonBy'],
                'Margin' : match['Margin'],   
                'Player_of_Match' : match['Player_of_Match'],   
                f'{match["Team1"]}' : match['Team1Players'],    
                f'{match["Team2"]}' : match['Team2Players'],  
                'Umpire1' : match['Umpire1'],
                'Umpire2' : match['Umpire2']
            })
    if len(matches) > 0:
        return {'Winnig Matches' : matches}
    return {'error':'does not won any match'}

# Function to get matches by venue
def matches_by_venue(venue_name):
    venue_matches = []
    for idx,match in df.iterrows():
        if match['Venue'] == venue_name:
            venue_matches.append({
                'ID': idx,
                "city": match['City'],
                "date": match['Date'],
                "team1": match['Team1'],
                "team2": match['Team2'],
                "winning_team": match['WinningTeam']
            })
    if len(venue_matches) > 0:
        return {venue_name : venue_matches}
    return {venue_name : 'No Match Found'}

# Function to get player of match performance
def player_of_match_performance(player_name):
    player_matches = []
    for idx,match in df.iterrows():
        if match['Player_of_Match'] == player_name:
            player_matches.append({
                "ID" : idx,
                "date" : match['Date'],
                "Venue" : match['Venue'],
                "winning_team": match['WinningTeam'],
                "won_by": match['WonBy'],
                "margin": match['Margin']
            })
    if len(player_matches) > 0:
        return {player_name : player_matches}
    return {'error' : 'no match found'}

# Function to get toss decision analysis
def toss_decision_analysis():
    if df.empty:
        return {
            "chooses bat and wins": 0,
            "chooses field and wins": 0,
            "total_matches": 0
        }

    # Filter matches where TossWinner is also the WinningTeam
    winning_toss = df[df['TossWinner'] == df['WinningTeam']]

    # Count occurrences of each TossDecision
    decision_counts = winning_toss['TossDecision'].value_counts()

    return {
        "chooses bat and wins": int(decision_counts.get('bat', 0)),
        "chooses field and wins": int(decision_counts.get('field', 0)),
        "total_matches": len(df)
    }

# Function to get head to head matches
def head_to_head(team1, team2):
    # Filter head-to-head matches
    head_to_head_matches = df[
        ((df['Team1'] == team1) & (df['Team2'] == team2)) |
        ((df['Team1'] == team2) & (df['Team2'] == team1))
    ].copy()

    if head_to_head_matches.empty:
        return {
            "total_matches": 0,
            "matches": [],
            "win_count": {team1: 0, team2: 0},
            "win_percentage": {team1: "0%", team2: "0%"},
            "close_matches": 0,
            "super_over_count": 0,
            "last_winner": "No matches played"
        }

    # Count wins for each team
    win_counts = {team1: 0, team2: 0}
    for _, match in head_to_head_matches.iterrows():
        winner = match['WinningTeam']
        if winner == team1:
            win_counts[team1] += 1
        elif winner == team2:
            win_counts[team2] += 1

    total_matches = len(head_to_head_matches)

    # Calculate win percentage
    def win_percentage(wins, total):
        return f"{round((wins / total) * 100, 2)}%" if total > 0 else "0%"

    win_percentages = {
        team1: win_percentage(win_counts[team1], total_matches),
        team2: win_percentage(win_counts[team2], total_matches)
    }

    # Count close matches (won by ≤10 runs or ≤5 wickets)
    close_matches = sum(
        (match['WonBy'] == "Runs" and int(match['Margin']) <= 10) or
        (match['WonBy'] == "Wickets" and int(match['Margin']) <= 5)
        for _, match in head_to_head_matches.iterrows()
    )

    # Count Super Over matches
    super_over_count = sum(match['SuperOver'] == 'Y' for _, match in head_to_head_matches.iterrows())

    # Get last match winner
    last_match = head_to_head_matches.iloc[-1]
    last_winner = last_match['WinningTeam']

    # Convert match data to list format
    matches_list = []
    for idx, match in head_to_head_matches.iterrows():
        matches_list.append({
            'ID': idx,
            'Date': match['Date'],
            'MatchNumber': match['MatchNumber'],
            'Venue': match['Venue'],
            'TossWinner': match['TossWinner'],
            'TossDecision': match['TossDecision'],
            'SuperOver': 'No' if match['SuperOver'] == 'N' else 'Yes',
            'WonBy': match['WonBy'],
            'Margin': match['Margin'],
            'Player_of_Match': match['Player_of_Match'],
            team1: match['Team1Players'],
            team2: match['Team2Players'],
            'Umpire1': match['Umpire1'],
            'Umpire2': match['Umpire2']
        })

    return {
        "total_matches": total_matches,
        "matches": matches_list,
        "win_count": win_counts,
        "win_percentage": win_percentages,
        "close_matches": close_matches,
        "super_over_count": super_over_count,
        "last_winner": last_winner
    }

# Function to get matches by margin
def matches_by_margin(margin_type, margin_value):
    if margin_type not in ['Runs','Wickets']:
        return {'error':'Invalid Winning type'}
    
    # Filter matches meeting the margin criteria
    filtered_data = df.loc[(df['WonBy'] == margin_type) & (df['Margin'] >= margin_value)]
    
    if filtered_data.empty:
        return {
            "total_matches": 0,
            "average_margin": None,
            "top_winning_team": None,
            "matches": []
        }

    # Extract relevant match details
    margin_matches = filtered_data[['WinningTeam', 'Margin']].to_dict(orient='records')

    # Additional analysis
    total_matches = len(filtered_data)
    avg_margin = filtered_data['Margin'].mean()
    top_winning_team = filtered_data['WinningTeam'].mode()[0]  # Most frequent winning team

    return {
        "total_matches": total_matches,
        "average_margin": float(round(avg_margin, 2)),
        "top_winning_team": top_winning_team,
        "matches": margin_matches
    }

# Function to get player matches
def player_matches(player_name):
    # Explode the lists in Team1Players and Team2Players
    df_exploded = df.copy()
    df_exploded = df_exploded.explode(['Team1Players','Team2Players'])

    # Filter matches where the player participated
    player_matches = df_exploded[
        (df_exploded['Team1Players'] == player_name) | (df_exploded['Team2Players'] == player_name)
    ].drop_duplicates()

    # Return default values if no matches found
    if player_matches.empty:
        return {
            "total_matches": 0,
            "win_percentage": None,
            "matches_won": 0,
            "matches_lost": 0,
            "opponents_faced": [],
            "super_over_matches": 0,
            "top_venues": [],
            "matches": []
        }
    
    # Determine player's team & opponent using vectorized operations
    player_matches["team"] = player_matches.apply(
        lambda row: row["Team1"] if row["Team1Players"] == player_name else row["Team2"], axis=1
    )
    player_matches["opponent"] = player_matches.apply(
        lambda row: row["Team2"] if row["team"] == row["Team1"] else row["Team1"], axis=1
    )

    # Determine match result using vectorized comparison
    player_matches["result"] = player_matches["WinningTeam"] == player_matches["team"]
    player_matches["result"] = player_matches["result"].map({True: "Won", False: "Lost"})

    # Count wins & losses
    match_results = player_matches["result"].value_counts()
    matches_won = match_results.get("Won", 0)
    matches_lost = match_results.get("Lost", 0)
    total_matches = matches_won + matches_lost
    win_percentage = round((matches_won / total_matches) * 100, 2) if total_matches > 0 else None

    # Count unique opponents
    opponents_faced = player_matches["opponent"].unique().tolist()

    # Count super over matches
    super_over_matches = (player_matches["SuperOver"] == "Y").sum()

    # Find top 3 venues
    top_venues = player_matches["Venue"].value_counts().head(3).index.tolist()

    # Extract match details
    match_details = player_matches[[
        "team", "opponent", "Venue", "result", "Margin", "WonBy", "Player_of_Match"
    ]].copy()

    # Format margin
    match_details["margin"] = match_details.apply(
        lambda row: f"{row['Margin']} {row['WonBy']}" if pd.notna(row["WonBy"]) else "N/A", axis=1
    )

    # Check if player was Player of the Match
    match_details["player_of_match"] = match_details["Player_of_Match"] == player_name
    match_details.drop(columns=["Player_of_Match", "WonBy", "Margin"], inplace=True)

    # Rename columns
    match_details.rename(columns={"Venue": "venue"}, inplace=True)

    return {
        player_name:
        {"total_matches": int(total_matches),
        "win_percentage": float(win_percentage),
        "matches_won": int(matches_won),
        "matches_lost": int(matches_lost),
        "opponents_faced": opponents_faced,
        "super_over_matches": int(super_over_matches),
        "top_venues": top_venues,
        "matches": match_details.to_dict(orient="records")}
    }

# Function to get matches by season (like '2020/21', '2019', etc.)
def matches_by_season(season_year):
    # Filter matches for the given season
    season_matches = df[df['Season'] == season_year]
    
    # Extract relevant match details
    matches_list = season_matches.apply(lambda match: {
        "date": match['Date'],
        "team1": match['Team1'],
        "team2": match['Team2'],
        "winning_team": match['WinningTeam'],
        "match_type": match['MatchNumber']
    }, axis=1).tolist()
    
    # Find the final match
    final_match = season_matches[season_matches['MatchNumber'] == 'Final']
    
    # Extract final match details
    final_match_details = None
    final_winner = None
    
    if not final_match.empty:
        final_match_details = {
            "date": final_match.iloc[0]['Date'],
            "team1": final_match.iloc[0]['Team1'],
            "team2": final_match.iloc[0]['Team2'],
            "winning_team": final_match.iloc[0]['WinningTeam'],
            "venue": final_match.iloc[0]['Venue'],
            "player_of_match": final_match.iloc[0]['Player_of_Match']
        }
        final_winner = final_match.iloc[0]['WinningTeam']
    
    # Player with the most "Player of the Match" awards
    player_of_match_counts = season_matches['Player_of_Match'].value_counts()
    top_player = player_of_match_counts.head(3).to_dict() if not player_of_match_counts.empty else None
    
    # Team performance (matches won, lost, win rate)
    teams = pd.concat([season_matches['Team1'], season_matches['Team2']]).unique()
    team_performance = {}
    
    for team in teams:
        matches_played = season_matches[(season_matches['Team1'] == team) | (season_matches['Team2'] == team)]
        matches_won = season_matches[season_matches['WinningTeam'] == team]
        matches_lost = matches_played.shape[0] - matches_won.shape[0]
        win_rate = (matches_won.shape[0] / matches_played.shape[0]) * 100 if matches_played.shape[0] > 0 else 0
        
        team_performance[team] = {
            "matches_played": matches_played.shape[0],
            "matches_won": matches_won.shape[0],
            "matches_lost": matches_lost,
            "win_rate": round(win_rate, 2)
        }
    
    # Venue that hosted the most matches
    venue_counts = season_matches['Venue'].value_counts()
    top_venue = venue_counts.head(3).to_dict() if not venue_counts.empty else None
    
    return {
        "season": season_year,
        "matches": matches_list,
        "final_match": final_match_details,
        "final_winner": final_winner,
        "top_player_of_match": top_player,
        "team_performance": team_performance,
        "top_venue": top_venue
    }

# Function to get Super Over matches
def super_over_matches():
    # Filter matches that had a Super Over
    super_over_df = df[df['SuperOver'] == 'Y']
    
    # List of all Super Over matches
    super_over_matches = super_over_df.apply(lambda match: {
        "season": match['Season'],
        "city": match['City'],
        "date": match['Date'],
        "team1": match['Team1'],
        "team2": match['Team2'],
        "winning_team": match['WinningTeam'],
        "venue": match['Venue']
    }, axis=1).tolist()

    # Count of Super Over matches per season
    super_over_per_season = super_over_df['Season'].value_counts().to_dict()

    # Team performance in Super Overs
    teams = pd.concat([super_over_df['Team1'], super_over_df['Team2']]).unique()
    super_over_team_stats = {}

    for team in teams:
        matches_played = super_over_df[(super_over_df['Team1'] == team) | (super_over_df['Team2'] == team)].shape[0]
        matches_won = super_over_df[super_over_df['WinningTeam'] == team].shape[0]

        super_over_team_stats[team] = {
            "super_over_played": matches_played,
            "super_over_won": matches_won,
            "win_rate": round((matches_won / matches_played) * 100, 2) if matches_played > 0 else 0
        }

    # Most frequent Super Over venue
    if not super_over_df.empty:
        most_frequent_venue = super_over_df['Venue'].value_counts().idxmax()
        most_frequent_venue_count = super_over_df['Venue'].value_counts().max()
    else:
        most_frequent_venue = None
        most_frequent_venue_count = 0

    # Most thrilling Super Over match-up (teams that played Super Over the most)
    matchups = super_over_df.apply(lambda row: tuple(sorted([row['Team1'], row['Team2']])), axis=1)
    most_common_matchup = matchups.value_counts().idxmax() if not matchups.empty else None
    most_common_matchup_count = matchups.value_counts().max() if not matchups.empty else 0

    return {
        "total_super_over_matches": len(super_over_matches),
        "super_over_matches": super_over_matches,
        "super_over_per_season": super_over_per_season,
        "team_super_over_performance": super_over_team_stats,
        "most_frequent_super_over_venue": {
            "venue": most_frequent_venue,
            "matches_hosted": int(most_frequent_venue_count)
        },
        "most_thrilling_super_over_rivalry": {
            "teams": most_common_matchup,
            "times_faced": int(most_common_matchup_count)
        }
    }

# Function to get highest margin matches
def highest_margin_matches():
    # Convert numeric columns if needed
    df['Margin'] = pd.to_numeric(df['Margin'], errors='coerce')

    # Separate highest wins by runs and wickets
    max_run_margin = df[df['WonBy'] == 'Runs']['Margin'].max()
    max_wicket_margin = df[df['WonBy'] == 'Wickets']['Margin'].max()

    # Get matches with highest run margin
    highest_run_margin_matches = df[(df['WonBy'] == 'Runs') & (df['Margin'] == max_run_margin)].apply(lambda match: {
        "season": match['Season'],
        "winning_team": match['WinningTeam'],
        "won_by": match['WonBy'],
        "margin": match['Margin'],
        "opponent": match['Team1'] if match['WinningTeam'] != match['Team1'] else match['Team2'],
        "venue": match['Venue']
    }, axis=1).tolist()

    # Get matches with highest wicket margin
    highest_wicket_margin_matches = df[(df['WonBy'] == 'Wickets') & (df['Margin'] == max_wicket_margin)].apply(lambda match: {
        "season": match['Season'],
        "winning_team": match['WinningTeam'],
        "won_by": match['WonBy'],
        "margin": match['Margin'],
        "opponent": match['Team1'] if match['WinningTeam'] != match['Team1'] else match['Team2'],
        "venue": match['Venue']
    }, axis=1).tolist()

    # Calculate average winning margin separately for "Runs" and "Wickets"
    dominant_teams_runs = df[df['WonBy'] == 'Runs'].groupby('WinningTeam')['Margin'].mean().sort_values(ascending=False).to_dict()
    dominant_teams_wickets = df[df['WonBy'] == 'Wickets'].groupby('WinningTeam')['Margin'].mean().sort_values(ascending=False).to_dict()

    # Count how many times each team won by a large margin (let's say 50+ runs or 8+ wickets)
    large_margin_wins = df[((df['WonBy'] == 'Runs') & (df['Margin'] >= 50)) | 
                            ((df['WonBy'] == 'Wickets') & (df['Margin'] >= 8))]['WinningTeam'].value_counts().to_dict()

    # Find the venue where highest margin wins occurred the most
    venue_max_margin = df[df['Margin'].isin([max_run_margin, max_wicket_margin])]['Venue'].value_counts()
    most_frequent_high_margin_venue = venue_max_margin.idxmax() if not venue_max_margin.empty else None
    most_frequent_high_margin_count = venue_max_margin.max() if not venue_max_margin.empty else 0

    return {
        "highest_run_margin": max_run_margin,
        "highest_wicket_margin": max_wicket_margin,
        "highest_margin_matches_by_runs": highest_run_margin_matches,
        "highest_margin_matches_by_wickets": highest_wicket_margin_matches,
        "most_dominant_teams_by_runs": dominant_teams_runs,
        "most_dominant_teams_by_wickets": dominant_teams_wickets,
        "teams_with_most_large_margin_wins": large_margin_wins,
        "most_frequent_high_margin_venue": {
            "venue": most_frequent_high_margin_venue,
            "times_hosted": int(most_frequent_high_margin_count)
        }
    }

# Function to get season analysis
def season_summary(season_year):
    season_matches = df[df['Season'] == season_year]
    if season_matches.empty:
        return {"error": "Season not found"}
    
    total_matches = len(season_matches)
    teams = list(set(season_matches['Team1'].tolist() + season_matches['Team2'].tolist()))
    venues = season_matches['Venue'].nunique()
    player_of_match_counts = season_matches['Player_of_Match'].value_counts().head(5).to_dict()
    winner = season_matches.iloc[0]['WinningTeam']
    return {
        "season": season_year,
        "total_matches": total_matches,
        "teams": teams,
        "Winner": winner,
        "unique_venues": venues,
        "top_players_of_match": player_of_match_counts
    }

# Function to get team performance over seasons
def team_performance_over_seasons(team):
    team_matches = df[(df['Team1'] == team) | (df['Team2'] == team)]
    if team_matches.empty:
        return {"error": "Team not found"}
    
    performance = {}
    total_final_played,total_final_wins = 0,0
    for season in sorted(team_matches['Season'].unique()):
        season_matches = team_matches[team_matches['Season'] == season]
        matches_played = len(season_matches)
        wins_in_season = season_matches[season_matches['WinningTeam'] == team]
        matches_won = len(wins_in_season)
        # we have put "NoResults" for ties 
        matches_lost = len(season_matches[(season_matches['WinningTeam'] != team) & (season_matches['WinningTeam'] != "NoResults")])
        ties = len(season_matches[season_matches['WinningTeam']=="NoResults"])  # If ties exist
        win_rate = (matches_won / matches_played) * 100 if matches_played > 0 else 0
    
        
        avg_margin_of_victory_by_runs = wins_in_season[wins_in_season['WonBy'] == "Runs"]['Margin'].mean()
        avg_margin_of_victory_by_wickets = wins_in_season[wins_in_season['WonBy'] == "Wickets"]['Margin'].mean()
        # team1, team2, winner = season_matches.iloc[0]['Team1'], season_matches.iloc[0]['Team2'], season_matches.iloc[0]['WinningTeam']
        final_match = season_matches[season_matches['MatchNumber'] == "Final"]
        was_in_final = False
        final_winner = False
        if not final_match.empty:
            was_in_final = True
            total_final_played+=1
            if not final_match[final_match['WinningTeam']==team].empty:
                final_winner = True
                total_final_wins+=1            
    
        performance[season] = {
            "matches_played": matches_played,
            "matches_won": matches_won,
            "matches_lost": matches_lost,
            "ties": ties,
            "was_in_final": was_in_final,
            "final_winner": final_winner,
            "avg_margin_of_victory_by_runs": float(round(avg_margin_of_victory_by_runs, 2)) if avg_margin_of_victory_by_runs is not None else None,
            "avg_margin_of_victory_by_wickets": float(round(avg_margin_of_victory_by_wickets, 2)) if avg_margin_of_victory_by_wickets is not None else None
        }
    
    return {team: {
        'performance' : performance,
        'total_final_played' : total_final_played,
        'total_final_wins' : total_final_wins
    }}

# Function to get Player Career Summary
def player_career_summary(player_name):
    # Filter matches where the player participated
    player_matches = df[
        df['Team1Players'].apply(lambda x: player_name in x) |
        df['Team2Players'].apply(lambda x: player_name in x)
    ]

    if player_matches.empty:
        return {"error": "Player not found"}   

    # Count total matches played
    total_matches_played = len(player_matches)

    # Count matches won by the player's team
    matches_won_by_team = player_matches.apply(
        lambda row: row['WinningTeam'] == (row['Team1'] if player_name in row['Team1Players'] else row['Team2']),
        axis=1
    ).sum()
    player_of_match = len(player_matches[player_matches['Player_of_Match'] == player_name])
    
     # Win percentage
    win_percentage = round((matches_won_by_team / total_matches_played) * 100, 2) if total_matches_played > 0 else 0

    # Teams played for
    teams_played_for = set(
        player_matches.apply(lambda row: row['Team1'] if player_name in row['Team1Players'] else row['Team2'], axis=1)
    )

    # Performance across seasons
    season_wise_stats = player_matches.groupby('Season').apply(
        lambda x: {
            "team": x.iloc[0]['Team1'] if player_name in x.iloc[0]['Team1Players'] else x.iloc[0]['Team2'],  # Extract team name
            "matches_played": len(x),
            "matches_won_by_team": int((x['WinningTeam'] == (x.iloc[0]['Team1'] if player_name in x.iloc[0]['Team1Players'] else x.iloc[0]['Team2'])).sum()),
            "win_rate": float(round((x['WinningTeam'] == (x.iloc[0]['Team1'] if player_name in x.iloc[0]['Team1Players'] else x.iloc[0]['Team2'])).sum() / len(x) * 100, 2))
        }
    ).to_dict()

    # Performance in finals
    finals_matches = player_matches[player_matches['MatchNumber'] == 'Final']
    finals_won = finals_matches.apply(
        lambda row: row['WinningTeam'] == (row['Team1'] if player_name in row['Team1Players'] else row['Team2']), axis=1
    ).sum()    

    return {
        "player_name": player_name,
        "total_matches_played": total_matches_played,
        "matches_won_by_team": int(matches_won_by_team),
        "win_percentage": win_percentage,
        "player_of_match_awards": player_of_match,
        "teams_played_for": list(teams_played_for),
        "season_wise_performance": season_wise_stats,
        "finals_played": len(finals_matches),
        "finals_won": int(finals_won)
    }
# IPL Match Analysis API

## Overview

This project provides a Flask-based API to analyze IPL match data. It enables users to retrieve various statistics, including match summaries, team performances, player achievements, and season-based insights.

## Features

- Retrieve a list of all teams
- Get match summary by match ID
- Find matches won by a specific team
- Get matches played at a particular venue
- Analyze player of the match performances
- Study toss decision outcomes and their impact
- Head-to-head analysis between two teams
- Analyze match-winning margins
- Fetch player-specific match details
- Get season-wise match insights
- Identify matches decided by Super Overs
- Find the highest-margin victories
- Get a summary of an IPL season
- Analyze team performance over multiple seasons
- Retrieve a player's career summary

## Technologies Used

- **Python** (Data processing and API logic)
- **Flask** (API framework)
- **Pandas** (Data manipulation)

## Setup Instructions

### Prerequisites

- Python 3.x
- Required Python libraries: `flask`, `pandas`

### Installation

1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd <repository_folder>
   ```
2. Install dependencies:
   ```sh
   pip install flask pandas
   ```
3. Ensure the dataset file (`IPL_dataset_cleaned.csv`) is present in the project directory.

### Running the API

Start the Flask server:

```sh
python app.py
```

The API will be accessible at `http://127.0.0.1:5000/`.

## API Endpoints

| Endpoint                         | Method | Query Parameters        | Description                                                     |
| -------------------------------- | ------ | ----------------------- | --------------------------------------------------------------- |
| `/teams`                         | GET    | None                    | Returns a list of IPL teams.                                    |
| `/match_summary`                 | GET    | `match_id`              | Returns match summary for the given match ID.                   |
| `/match_won_by_team`             | GET    | `team`                  | Fetches all matches won by a specific team.                     |
| `/matches_by_venue`              | GET    | `venue`                 | Retrieves matches played at a given venue.                      |
| `/player_of_match_performance`   | GET    | `player`                | Fetches performances of a player awarded "Player of the Match." |
| `/toss_decision_analysis`        | GET    | None                    | Analyzes toss decisions and winning patterns.                   |
| `/head_to_head`                  | GET    | `team1`, `team2`        | Shows head-to-head statistics between two teams.                |
| `/matches_by_margin`             | GET    | `margin_type`, `margin` | Finds matches won by a specific margin (Runs/Wickets).          |
| `/player_matches`                | GET    | `player`                | Retrieves all matches in which a player participated.           |
| `/season_analysis`               | GET    | `season`                | Fetches season-wise match details.                              |
| `/super_over_matches`            | GET    | None                    | Lists all Super Over matches.                                   |
| `/highest_margin_matches`        | GET    | None                    | Provides details on matches with the highest victory margins.   |
| `/season_summary`                | GET    | `season`                | Gives an overview of a particular IPL season.                   |
| `/team_performance_over_seasons` | GET    | `team`                  | Analyzes a team's performance across multiple seasons.          |
| `/player_career_summary`         | GET    | `player`                | Fetches a player's career performance summary.                  |

## Example Usage

**Get the list of IPL teams:**

```sh
curl -X GET "http://127.0.0.1:5000/teams"
```

**Fetch match summary by match ID:**

```sh
curl -X GET "http://127.0.0.1:5000/match_summary?match_id=123"
```

**Retrieve all matches won by a team:**

```sh
curl -X GET "http://127.0.0.1:5000/match_won_by_team?team=Mumbai%20Indians"
```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -m 'Add new feature'`).
4. Push the changes (`git push origin feature-branch`).
5. Submit a pull request.

## License

This project is open-source.


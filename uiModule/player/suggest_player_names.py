from fuzzywuzzy import process

def suggest_player_names(df, player_name):
    """Suggest player names based on user input."""
    players = df['PLAYER'].unique()
    suggestions = process.extract(player_name, players, limit=5)
    return [name for name, score in suggestions if score > 50]

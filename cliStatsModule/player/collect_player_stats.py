def collect_player_stats(df, player_name, row_count):
    """Collect stats for a specified player."""
    player_stats = df[df['PLAYER'].str.contains(player_name, case=False, na=False)]
    if player_stats.empty:
        print(f"No stats found for player '{player_name}'.")
        return None
    return player_stats.head(row_count)

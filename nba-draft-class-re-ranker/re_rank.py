POINTS_WEIGHT = 0.6
ASSISTS_WEIGHT = 0.3
REBOUNDS_WEIGHT = 0.1

DEFAULT_CRITERIA = [
  {'category': 'per_game-PTS', 'weight': POINTS_WEIGHT},
  {'category': "per_game-AST", 'weight': ASSISTS_WEIGHT},
  {'category': "per_game-TRB", 'weight': REBOUNDS_WEIGHT}
]

def re_rank_stat_table(stats: list[dict]) -> list[dict]:
  
 return sorted(stats, key=lambda player: player['par_rank'], reverse=True)



# Get ranking score
def get_ranking_value(player_dict: dict, criteria: list[dict]= DEFAULT_CRITERIA) -> float:
  
  ranking_value = 0

  for criterion in criteria:

    try:
      ranking_value = ranking_value + (float(player_dict[criterion['category']]) * criterion['weight'])
    
    except:
      ranking_value = ranking_value

  return (round(ranking_value, 2))
 
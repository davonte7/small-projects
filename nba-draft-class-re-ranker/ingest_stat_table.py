from bs4 import BeautifulSoup, NavigableString, Tag
from get_stat_table import get_stat_year
from re_rank import re_rank_stat_table, get_ranking_value

NEW_FILE_NAME = "new_ranks.html"

# format the stats
def ingest_table(soup: NavigableString) -> list[dict]:

  table_head = soup.find('thead')

  # Flatten and Remove the Over Header
  round_header = table_head.find('tr',class_='over_header')

  # Flattened Row
  flattened_row = []

  for th in round_header.find_all('th'):
    text = th.text.strip()
    colspan = int(th.get('colspan',1))
    flattened_row.extend([text]*colspan)
  
  round_header.decompose()

  # Get Headers
  row_headers = table_head.find_all('th')

  rows = [row for row in soup.find_all('tr') if len(row.find_all('td')) > 0]

  player_dicts = []
  for row in rows:
    cells = row.find_all(['td','th'])

    player_dict = {}
    for round_header,category,value in zip(flattened_row, row_headers, cells):
      
      cat_text = category.get_text(strip=True)
      formatted_round_header = round_header.lower().replace(" ", "_")

      if cat_text in player_dict:
        player_dict[formatted_round_header+"-"+cat_text] = value.get_text(strip=True)
      else:
        player_dict[cat_text] = value.get_text(strip=True)

    player_dict["par_rank"] = get_ranking_value(player_dict)
    player_dicts.append(player_dict)
    
  return player_dicts

# Sort stats based on criteria
def sort_by_par(stats: list[dict]) -> list[dict]:
  return sorted(stats, key=get_ranking_value, reverse=True)

def format_table(stats = list[dict]):

  new_soup = BeautifulSoup("<body> </body>", "lxml")
  body = new_soup.find('body')

  style = 'border: 1px solid black; padding: 5px;'

  new_table = new_soup.new_tag('table')
  new_table['style'] = 'border-collapse: collapse; border: 1px solid black;'

  new_thead = new_soup.new_tag('thead')

  header_row = new_soup.new_tag("tr")
  headers = ["Rank", "Player Name", "Games", "Score"]
  for header in headers:
      th = new_soup.new_tag("th")
      th['style'] = style
      th.string = header
      header_row.append(th)

  new_thead.append(header_row)
  new_table.append(new_thead)

  def get_cell(soup: BeautifulSoup, value:str) -> Tag:
    cell =  soup.new_tag('td')
    cell['style'] = style
    cell.string = value

    return cell

  for idx,player in enumerate(stats):
    row = new_soup.new_tag('tr')

    rank_number_cell = get_cell(new_soup, f"{str(idx+1)}")
    
    try:
      name_cell = get_cell(new_soup, player['Player'])
      game_cell = get_cell(new_soup, str(player['G']))
      rank_cell = get_cell(new_soup, str(player['par_rank']))
    
    except:
      print(f"Error Formatting Player {idx}")
      continue

    row.append(rank_number_cell)
    row.append(name_cell)
    row.append(game_cell)
    row.append(rank_cell)

    new_table.append(row)
    # print(new_table)

  body.append(new_table)
  return body

def rank(year:int):
  stat_table = get_stat_year(year)
  stats = ingest_table(stat_table)
  sorted_stats = re_rank_stat_table(stats)
  new_table = format_table(sorted_stats)


  with open(NEW_FILE_NAME, "w", encoding='charmap') as new_file:
    new_file.write(new_table.prettify())
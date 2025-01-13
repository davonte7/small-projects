import requests
from bs4 import BeautifulSoup, NavigableString

# Get stats from website
def get_stat_year(year:int) -> NavigableString:

  try: 
    response = requests.get(f"https://www.basketball-reference.com/draft/NBA_{year}.html", timeout=10)
    stat_html = response.text

    soup = BeautifulSoup(stat_html,"html.parser")
    table = soup.find('table', id='stats')

    return table

  except requests.exceptions.RequestException as e:
    print(f"Error accessing the URL: {e}")
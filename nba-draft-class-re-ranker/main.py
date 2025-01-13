import argparse
from ingest_stat_table import rank


# Take in CLI argument year
parser = argparse.ArgumentParser(description="A script that takes a year from the command line to re-rank draft classes.")
parser.add_argument('year', type=str, help="The year of the draft class.")
args = parser.parse_args()


# Takes in the following params
# Year
# Stats to Rank By and their weights
rank(args.year)

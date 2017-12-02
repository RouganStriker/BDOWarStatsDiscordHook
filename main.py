import argparse
import os

from bdo_stats import BDOStats

parser = argparse.ArgumentParser()
parser.add_argument("csv", help="CSV file")
parser.add_argument("--webhook", dest="webhook", help="Discord Webhook")
args = parser.parse_args()

if not os.path.exists(args.csv):
    raise Exception("CSV file does not exist")

webhook = args.webhook or os.environ.get('DISCORD_STATS_WEBHOOK')

date = raw_input("Enter the date (dd/mm/yyyy): ")
nodeName = raw_input("Enter the Node Name: ")
outcome = raw_input("Enter the outcome (win,loss,tie): ")

BDOStats(args.csv, webhook).generate_stats(nodeName, outcome, date)

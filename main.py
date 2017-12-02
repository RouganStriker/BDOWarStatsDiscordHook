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

BDOStats(args.csv, webhook).parse()

import argparse
import csv
import os

from .bdo_stats import BDOStats

parser = argparse.ArgumentParser()
parser.add_argument("csv", help="CSV file")
args = parser.parse_args()

if not os.path.exists(args.csv):
    raise Exception("CSV file does not exist")

BDOStats(args.csv).parse()

from collections import OrderedDict
import csv
import json
import numpy as np
import pandas as pd
import requests


class BDOStats(object):
    def __init__(self, csv_file):
        with open(csv_file) as f:
            rows = csv.reader(f)
            header = rows.next()
            if len(header) < 11:
                raise Exception("Expected at least 12 columns, got {0}".format(len(header)))

            self.stats = [[row[0]] + map(int, row[1:12]) for row in rows]
            self.column_data = OrderedDict([
                ('Fortress', {
                    'stats': [('max', 'Most')],
                    'verb': ' Destroyed',
                    'emoji': ':european_castle:',
                }),
                ('Command Post', {
                    'stats': [('max', 'Most')],
                    'verb': ' Destroyed',
                    'emoji': ':japanese_castle:',
                }),
                ('Gate', {
                    'stats': [('max', 'Most')],
                    'verb': ' Destroyed',
                    'emoji': ':shinto_shrine:',
                }),
                ('Help', {
                    'stats': [('max', 'Most'), ('min', 'Least')],
                    'verb': '',
                    'emoji': ':handshake:',
                }),
                ('Mount', {
                    'stats': [('max', 'Most'), ('min', 'Least')],
                    'verb': ' Kills',
                    'emoji': ':horse:',
                }),
                ('Placed Object', {
                    'stats': [('max', 'Most')],
                    'verb': ' Destroyed',
                    'emoji': ':hammer:',
                }),
                ('Guild Master', {
                    'stats': [('max', 'Most'), ('min', 'Least')],
                    'verb': ' Kills',
                    'emoji': ':prince:',
                }),
                ('Officer', {
                    'stats': [('max', 'Most'), ('min', 'Least')],
                    'verb': ' Kills',
                    'emoji': ':cop:',
                }),
                ('Member', {
                    'stats': [('max', 'Most'), ('min', 'Least')],
                    'verb': ' Kills',
                    'emoji': ':man_with_gua_pi_mao:',
                }),
                ('Deaths', {
                    'stats': [('max', 'Most'), ('min', 'Least')],
                    'verb': '',
                    'emoji': ':skull_crossbones:',
                }),
                ('Siege Weapons', {
                    'stats': [('max', 'Most'), ('min', 'Least')],
                    'verb': ' Kills',
                    'emoji': ':bomb:',
                }),
                ('Total', {
                    'stats': [('max', 'Most'), ('min', 'Least'), ('mean', 'Average')],
                    'verb': ' Kills',
                    'emoji': ':knife:',
                }),
                ('KDR', {
                    'stats': [('max', 'Most'), ('min', 'Least'), ('mean', 'Average')],
                    'verb': '',
                    'emoji': ':crossed_swords:',
                }),
            ])

    def get_summary(self, node_name, result):
        return {
            "node": node_name,
            "result": result,
            "attendanceCount": len(self.stats)
        }

    def parse(self):
        df = pd.DataFrame(self.stats, columns=['Player'] + self.column_data.keys()[:11])
        df['Total'] = df['Guild Master'] + df['Officer'] + df['Member'] + df['Siege Weapons']
        df['KDR'] = df['Total'].divide(df['Deaths'])
        df['KDR'].replace([np.inf, -np.inf], np.nan, inplace=True)
        df.set_index('Player', inplace=True)

        results = {
            'averages': [], # We display the averages in the summary panel
            'superlatives': []
        }

        for col, data in self.column_data.items():
            field_values = []

            for stat, adjective in data['stats']:
                if stat == 'max':
                    value = df[col].max()
                elif stat == 'min':
                    value = df[col].min()
                elif stat == 'mean':
                    value = df[col].mean()
                else:
                    raise Exception("Unknown stat {0}".format(stat))

                if value == 0:
                    players = ''
                else:
                    # List the player names
                    players = " ({})".format(", ".join(df.iloc[np.where(df[col] == value)[0]].index.tolist()))

                if stat == 'mean':
                    results['averages'].append(
                        '{emoji} Average {col}{verb}: {value}{players}'.format(emoji=data['emoji'],
                                                                               col=col,
                                                                               verb=data['verb'],
                                                                               value=value,
                                                                               players=players)
                    )
                else:
                    field_values.append(
                        '{adjective}{verb}: {value}{players}'.format(adjective=adjective,
                                                                     verb=data['verb'],
                                                                     value=value,
                                                                     players=players)
                    )

            results['superlatives'].append({
                'name': '{emoji} {col}{verb}'.format(emoji=data['emoji'],
                                                      col=col,
                                                      verb=data['verb']),
                'value': '\n'.join(field_values),
            })

        data = {
            "content": "@everyone",
            "embeds": [
                {
                    "title": "Node War Summary",
                    "fields": [
                        {
                            "name": "Attendance Count",
                            "value": len(self.stats)
                        }
                    ]
                },
                {
                    "title": "Node War Stats",
                    "fields": results['superlatives']
                }
            ]
        }
        requests.post('https://discordapp.com/api/webhooks/386422713813565440/wUDlTkdTbYiSOFBDtXhFdA6St91NH0DxEfCsrxthzBwJB_4JAe9XDwH6Ip0qKP2dt8Tn', data=data)

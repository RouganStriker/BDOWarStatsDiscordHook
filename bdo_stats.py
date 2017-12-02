from collections import OrderedDict
import csv
import numpy as np
import pandas as pd


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
                    'verb': ' Kills',
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
            'superlatives': {}
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

            results['superlatives'][col] = {
                'name': '{emoji} {col}{verb}'.format(emoji=data['emoji'],
                                                      col=col,
                                                      verb=data['verb']),
                'value': '\n'.join(field_values),
            }

        print(results)

            #
            # if col in ['Fortress', 'Command Post', 'Gate', 'Placed Objects']:
            #     # We only care about the max and ignore 0
            #     highest = df[col].max()
            #     if highest == 0:
            #         result = 0
            #     else:
            #         result = "{0} ({1})".format(highest, ", ".join(get_players(col, highest)))
            #     print("Most {0} Destroyed: {1}".format(col, result))
            # else:
            #     highest = df[col].max()
            #     lowest = df[col].min()
            #     avg = df[col].mean()
            #
            #     if col in ["Deaths", "Help", 'KDR']:
            #         descriptor = ""
            #     else:
            #         descriptor = "Kills"
            #
            #     if highest == 0:
            #         print("Most {0} {1}: 0".format(col, descriptor))
            #     else:
            #         print("Most {0} {1}: {2} ({3})".format(col, descriptor, highest,
            #                                                ", ".join(get_players(col, highest))))
            #     if lowest == 0:
            #         result = 0
            #     else:
            #         result = "{1} ({2})".format(lowest, ", ".join(get_players(col, lowest)))
            #     print("Least {0} {1}: {2}".format(col, descriptor, lowest, result))
            #
            #     print("Average {0} {1}: {2}".format(col, descriptor, avg))



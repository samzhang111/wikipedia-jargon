from __future__ import print_function
import sys
import os
import pandas as pd
from tabulate import tabulate

def with_numbers(li):
    return ['%d. %s' % (i + 1, s) for i, s in enumerate(li)]

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('''Usage: python make_tables.py [term_diff_file1] [term_diff_file2] ...

Note the file names are expected to be in the form `[Subject]_td.csv`
                ''')
        sys.exit(1)

    files = sys.argv[1:]

    for f in files:
        subject = os.path.basename(f).split('_')[0]
        df = pd.read_csv(f)
        simple = df.term.head(10)
        jargon = df.term.tail(10)[::-1]

        table = tabulate(zip(with_numbers(simple), with_numbers(jargon)),
                headers=['Simplest (%s)' % subject, 'Jargonest (%s)' % subject],
                tablefmt='psql')

        print(table)
        print()

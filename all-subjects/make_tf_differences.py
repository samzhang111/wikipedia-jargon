from __future__ import print_function
import msgpack
import sys
import os
from collections import defaultdict
from helpers import text_dict_to_term_dict
from WikiExtractor import clean, compact
import pandas as pd

def remove_wikipedia_markup(text):
    return compact(clean(text.decode('utf8')))

def print_help_and_exit(msg=''):
    if msg:
        print('Error: {}\n'.format(msg))

    print('Usage: python make_tf_differences.py [n-grams] [path to directory]')
    print('The directory should contain files output by grab_texts.py')
    sys.exit(1)

if len(sys.argv) <= 2:
    print_help_and_exit()

##############################################################
# Read in msgpack files, separating them from simple and en Wikipedia
##############################################################
ngrams = int(sys.argv[1])
text_dir = sys.argv[2]

try:
    files = os.listdir(text_dir)
except OSError:
    print_help_and_exit()

##############################################################
# Organize the text files by subject, then wiki (en or simple)
##############################################################
file_dict = defaultdict(dict)
for f in files:
    try:
        subject, wiki, _ = f.split('_')
        file_dict[subject][wiki] = f
    except ValueError:
        print_help_and_exit('Text directory does not contain valid filenames')

for subject in file_dict:
    print('Importing ', subject)
    with open(os.path.join(text_dir, file_dict[subject]['en'])) as f:
        en_text = msgpack.load(f)
        en_text = {k: remove_wikipedia_markup(v) for k,v in en_text.items()}

    with open(os.path.join(text_dir, file_dict[subject]['simple'])) as f:
        sm_text = msgpack.load(f)
        sm_text = {k: remove_wikipedia_markup(v) for k,v in sm_text.items()}

    print('Calculating term differences')
    en_tf, en_counts = text_dict_to_term_dict(en_text, ngrams)
    sm_tf, sm_counts = text_dict_to_term_dict(sm_text, ngrams)

    sm_terms = set(sm_tf)
    en_terms = set(en_tf)
    term_differences = {}

    for t in sm_terms.union(en_terms):
        term_differences[t] = en_tf[t] - sm_tf[t]

    sorted_term_difference = sorted(term_differences.items(),
            key=lambda x: x[1])

    print('Outputting term differences')
    td_df = pd.DataFrame(sorted_term_difference, columns=['term',
        'term_difference'])

    td_df['en_tf'] = td_df.term.apply(lambda x: en_tf[x])
    td_df['sm_tf'] = td_df.term.apply(lambda x: sm_tf[x])

    try:
        os.mkdir('term-diffs/ngrams-{}'.format(ngrams))
    except OSError:
        pass

    td_df.to_csv('term-diffs/ngrams-{}/{}_td.csv'.format(ngrams, subject),
            index=False, encoding='utf8')


from __future__ import print_function
import os
import sys
import codecs
from get_category_text import all_pages_in_wiki

if len(sys.argv) < 2:
    print("Usage: python grab_subjects.py [Subject1] [Subject2] [...]")
    print("For example, python grab_subjects.py Mathematics Economics")
    sys.exit(1)

subjects = sys.argv[1:]
print('All categories: ', subjects)
for s in subjects:
    all_titles = all_pages_in_wiki("Category: " + s)
    fn = os.path.join('data', s + '_titles.txt')
    with codecs.open(fn, 'w', 'utf-8') as out:
        out.write('\n'.join(all_titles))

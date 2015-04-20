from __future__ import print_function
import os
import sys
from get_category_text import page_content, simple_base, en_base
import msgpack

if len(sys.argv) < 2:
    print("Usage: python grab_subjects.py [Titlefile1] [Titlefile2] [...]")
    print("For example, python grab_subjects.py Mathematics_titles.txt")
    sys.exit(1)

files = sys.argv[1:]

print('Downloading text from: ', files)
for fn in files:
    with open(fn, 'r') as f:
        titles = [x.strip() for x in f]

    subject = os.path.basename(fn).split('_')[0]
    outfn_simple = os.path.join('data', 'text', subject + '_simple_text.msgpack')
    outfn_en = os.path.join('data', 'text', subject + '_en_text.msgpack')

    # Get raw content from both simple and regular Wikipedia
    simple_content = page_content(titles, simple_base)
    with open(outfn_simple, 'wb') as out:
        msgpack.pack(simple_content, out)

    en_content = page_content(titles, en_base)
    with open(outfn_en, 'wb') as out:
        msgpack.pack(en_content, out)

# coding: utf-8
from WikiExtractor import clean, compact
import xml.etree.ElementTree as ET
import sys
import cPickle as pickle

ns = {'export': 'http://www.mediawiki.org/xml/export-0.10/'}

def invalid_node(title, text):
    return title.startswith('Category:') or '{{disambiguation}}' in text

def prune_clean(sd, md):
    # Remove category and disambiguation pages
    to_delete = set()
    for title, val in sd.iteritems():
        if invalid_node(title, val):
            to_delete.add(title)

    for e in to_delete:
        del sd[e]

    for title, val in md.iteritems():
        if invalid_node(title, val):
            to_delete.add(title)

    for e in to_delete:
        if e in md:
            del md[e]
    # Remove pages that aren't in both datasets
    to_delete.update(set(sd).difference(set(md)))

    for e in to_delete:
        if e in sd:
            del sd[e]

        if e in md:
            del md[e]

    # Remove wiki markup.
    for k in sd:
        sd[k] = compact(clean(sd[k]))
        md[k] = compact(clean(md[k]))

def wiki_xml_to_dict(root):
    '''Reshapes wiki XML to dictionaries of {title: text}'''
    nodes = root.findall('export:page', ns)
    d = {}
    for n in nodes:
        d[n.find('export:title', ns).text] =\
            n.find('export:revision/export:text', ns).text

    return d

stree = ET.parse('simple-wiki-math.xml')
sroot = stree.getroot()
sd = wiki_xml_to_dict(sroot)

mtree = ET.parse('wiki-math.xml')
mroot = mtree.getroot()
md = wiki_xml_to_dict(mroot)

prune_clean(sd, md)

with open('simple.p', 'w') as f:
    pickle.dump(sd, f)
with open('math.p', 'w') as f:
    pickle.dump(md, f)

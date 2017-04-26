from __future__ import print_function
import requests
simple_base = u"https://simple.wikipedia.org/w/api.php"
en_base = u"https://en.wikipedia.org/w/api.php"

list_endpoint = u"?format=json&action=query&list=categorymembers&cmtitle={cat}&continue=-||&cmcontinue={cont}"
page_endpoint = u"?action=query&format=json&redirects&prop=revisions&rvprop=content&titles={titles}"

visited_categories = set()

def all_pages_in_wiki(category, wiki_base=simple_base):
    print(u"Crawling category {}".format(category))

    cont = ''
    all_pages = set()

    visited_categories.add(category)

    while True:
        rawresp = requests.post(wiki_base + list_endpoint.format(cat=category,
            cont=cont))

        resp = rawresp.json()
        if 'continue' not in resp:
            break

        for r in resp['query']['categorymembers']:
            # Is an article
            if r['ns'] == 0:
                all_pages.add(r['title'])

            # Is a previously unseen category?
            elif r['ns'] == 14 and r['title'] not in visited_categories:
                more_pages = all_pages_in_wiki(r['title'], wiki_base)
                all_pages.update(more_pages)

        cont = resp['continue']['cmcontinue']


    return all_pages

def page_content(pages, wiki_base=simple_base):
    ''' The response is structured like this:

{
    "query": {
        "pages": {
            "87837": {
                "pageid": 87837,
                "ns": 0,
                "title": "Ratio",
                "revisions": [
                    {
                        "contentformat": "text/x-wiki",
                        "contentmodel": "wikitext",
                        "*": "{{other uses}}\n{{redirect|is to|the ... }}"
                    }]
            }
            ....
        }
    }
}

    '''

    d = {}

    # GET requests have a max length.
    for i in range(0, len(pages), 30):
        print(u'Chunk {}/{}...: {}'.format(i, len(pages), pages[i].decode('utf8')))
        chunk = '|'.join(pages[i:min(i+30, len(pages))]).decode('utf-8', 'ignore')

        rawresp = requests.post(wiki_base + page_endpoint.format(titles=chunk))

        #rawresp = requests.post(wiki_base + page_endpoint, data=dict(titles=pages))
        resp = rawresp.json()


        ps = resp['query']['pages']
        for p in ps:
            title = ps[p]['title']
            try:
                raw_page = ps[p]['revisions'][0]['*']
            except KeyError:
                # No document
                continue

            d[title] = raw_page

    return d

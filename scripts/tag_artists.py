import argparse
import requests
import json
import time
from neo4j.v1 import GraphDatabase

TAG_TX = '''
MATCH (p:Page {title: $title})
SET p.artist = true
RETURN p
'''

WIKI_API_BASE = 'https://en.wikipedia.org/w/api.php'
WIKI_API_PARAMS = {
    'action': 'query',
    'list': 'categorymembers',
    'cmtitle': 'Category:Wikipedia articles with MusicBrainz identifiers',
    'cmlimit': 500,
    'format': 'json',
}


def parse_args():
    parser = argparse.ArgumentParser(
        description='Tag wikipedia article names with artist names')
    parser.add_argument('--neo4j_host', default='bolt://localhost',
                        help='Neo4j host, default \'bolt://localhost\'')
    parser.add_argument('--neo4j_user', default='neo4j',
                        help='Neo4j username, default \'neo4j\'')
    parser.add_argument('--neo4j_pw', help='Neo4j password')
    parser.add_argument('--outfile', default='artists.txt',
                        help='File to output a list of artists to')

    return parser.parse_args()


def tag_artist(tx, page_title):
    """Tag a page title as an artist in a neo4j transaction."""
    result = tx.run(TAG_TX, title=page_title)
    return result.single()[0]


def fetch_page(c={}):
    """Fetch a page and return the continue params."""
    response = requests.get(WIKI_API_BASE, params={**WIKI_API_PARAMS, **c})
    if response.status_code != 200:
        raise Exception(response.text)
    try:
        result = response.json()
        if 'error' in result:
            print(result['error'])
        if 'warnings' in result:
            print(result['warnings'])
        if 'query' in result:
            return result['query']['categorymembers'], result.get('continue')
    except json.decoder.JSONDecodeError:
        raise Exception(response.text)


if __name__ == '__main__':
    args = parse_args()
    count = 0
    c = {}

    n4j = GraphDatabase.driver(
        args.neo4j_host, auth=(args.neo4j_user, args.neo4j_pw))

    with open(args.outfile, 'a') as fh:
        with n4j.session() as session:
            while c is not None:
                pages, c = fetch_page(c)
                for page in pages:
                    title = page['title']
                    try:
                        session.write_transaction(tag_artist, title)
                    except TypeError:
                        print('TypeError processing {}'.format(title))
                    fh.write('{}\n'.format(title))
                count += len(pages)
                print(count)
                time.sleep(0.5)

            session.run('CREATE INDEX ON :Page(artist)')

    n4j.close()

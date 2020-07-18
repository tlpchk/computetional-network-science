import json
import re

import networkx as nx
import requests
import pandas as pd

AUTHOR_SEARCH = "https://api.elsevier.com/content/search/author"
PWD_ID_QUERY = 'AF-ID(60019987)'
FEMALE_NAMES = 'AUTHFIRST(*a)'
MALE_NAMES = 'not AUTHFIRST(*a)'
AND = ' and '

res = []


def add_nodes(graph: nx.Graph, url: str, params: dict):
    resp = json.loads(requests.get(url=url, params=params)
                      .text)['search-results']

    print(resp['opensearch:startIndex'])

    for author in resp['entry']:
        idx = re.sub('\D', '', author['dc:identifier'])
        name = (author['preferred-name']['surname'] +
                ' ' +
                author['preferred-name'].get('given-name', ''))
        citations_link = author['link'][2]['@href']
        graph.add_node(idx, name=name, cite=citations_link)
        res.append({
            'id': idx,
            'name': name,
            'citations': citations_link
        })

    if int(resp['opensearch:totalResults']) > (
            int(resp['opensearch:startIndex']) +
            int(resp['opensearch:itemsPerPage'])):
        for link in resp['link']:
            if link['@ref'] == 'next':
                add_nodes(
                    graph,
                    url=link['@href'],
                    params={'apiKey': params['apiKey']}
                )


with open('config.json') as config_file:
    config = json.load(config_file)

params = {'apiKey': config['api_key'],
          'count': 200,
          'query': PWD_ID_QUERY + AND + FEMALE_NAMES}

graph = nx.DiGraph()

add_nodes(graph, AUTHOR_SEARCH, params)

params['query'] = PWD_ID_QUERY + AND + MALE_NAMES

add_nodes(graph, AUTHOR_SEARCH, params)

print(graph.number_of_nodes())

res_df = pd.DataFrame(res)

res_df.to_csv('data/nodes.csv', index=False)


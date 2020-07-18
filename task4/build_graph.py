import time
from os import listdir
from os.path import isfile
from pathlib import Path

import networkx as nx
import pandas as pd
from pandas.errors import EmptyDataError

CITATIONS_DIR = Path('data/citations')
GRAPH_DIR = Path('data/graph')
NODES_FILE = Path('data/nodes.csv')

def build_graph(node_column):
    filenames = [filename for filename in listdir(CITATIONS_DIR) if isfile(CITATIONS_DIR / filename)]
    all_authors_df = pd.read_csv(NODES_FILE, index_col='id')

    graph = nx.DiGraph()
    node_names = all_authors_df.index if node_column == 'id' else all_authors_df[node_column]
    graph.add_nodes_from(node_names)

    tic = time.time()

    for idx, filename in enumerate(filenames):
        print(idx)
        try:
            cite_authors_data = pd.read_csv(CITATIONS_DIR / filename)
            author_id = filename[:-4]

            if 'Author(s) ID' not in cite_authors_data.columns or not author_id.isdigit():
                continue

            author_id = int(author_id)

            if author_id not in all_authors_df.index:
                continue

            for cite_authors_row in cite_authors_data['Author(s) ID']:
                cite_authors_ids = map(int,
                                       filter(lambda x: x.isdigit(),
                                              str(cite_authors_row).split(sep=';')))
                for cite_author_id in cite_authors_ids:
                    if cite_author_id in all_authors_df.index:
                        if node_column == 'id':
                            author = author_id
                            cite_author = cite_author_id
                        else:
                            author = all_authors_df.loc[author_id, node_column]
                            cite_author = all_authors_df.loc[cite_author_id, node_column]

                        if graph.has_edge(cite_author, author):
                            graph[cite_author][author]['weight'] += 1
                        else:
                            graph.add_edge(cite_author, author, weight=1)

        except EmptyDataError:
            pass

    print(time.time() - tic, 'seconds')
    return graph


if __name__ == '__main__':
    graph = build_graph('id')
    df = nx.to_pandas_edgelist(graph)
    df.to_csv(GRAPH_DIR / 'graph_id.csv', sep=';', index=None)

    graph = build_graph('name')
    df = nx.to_pandas_edgelist(graph)
    df.to_csv(GRAPH_DIR / 'graph_name.csv', sep=';', index=None)

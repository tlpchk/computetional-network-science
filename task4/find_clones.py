import re
from pathlib import Path

import networkx as nx
import pandas as pd

from build_graph import NODES_FILE, GRAPH_DIR

INPUT_GRAPH_PATH = GRAPH_DIR / 'graph_id.csv'
OUTPUT_NODES_PATH = Path('data/nodes_without_copies.csv')


def get_excessive_nodes(authors_path, graph_path):
    authors_df = pd.read_csv(authors_path, index_col='id')
    graph_df = pd.read_csv(graph_path, sep=';')
    graph = nx.from_pandas_edgelist(graph_df, edge_attr='weight', create_using=nx.DiGraph())
    similar_pairs, error_names = find_clones(authors_df['name'].values)
    result = []

    for pair in similar_pairs:
        a_dict = get_node_statistic(authors_df, graph, pair[0])
        b_dict = get_node_statistic(authors_df, graph, pair[1])

        print(f"{a_dict['name']} [in: {a_dict['in_d']}, out: {a_dict['out_d']}]"
              f" ~ {b_dict['name']} [in: {b_dict['in_d']}, out: {b_dict['out_d']}]")

        excessive_node = a_dict['id'] if a_dict['in_d'] < b_dict['out_d'] else b_dict['id']
        result.append(excessive_node)

    print(f"\n#Pairs of similar authors : {len(similar_pairs)}")
    print(f"#Nodes to remove : {len(result)}")

    return result


def find_clones(full_names):
    """Find authors with similar names
        Assertions :
            First word in column 'name' is surname
            Rest of words in column 'name' are names

        Similar authors :
            - have same surnames
            - have same number of names
            - have same order of names
                Nowak Jan Paweł !~ Nowak Paweł Jan
            - have same names in full or short form
                Nowak Jan Paweł ~ Nowak J. Paweł ~ Nowak J. P.

    """
    full_names = [str.strip(full_name) for full_name in full_names]
    full_names = [full_name.split(' ') for full_name in full_names]
    n = len(full_names)
    similar = []
    errors = []

    for i in range(n):
        try:
            # surname, [name1, name2 ... ]
            a_surname, a_names = full_names[i][0], full_names[i][1:]
            a_first_letters = [name[0] for name in a_names]

            # Jan Paweł -> ^[J|P].?$
            re_short_name = re.compile(fr'^[{"|".join(a_first_letters)}]\.?$')
            # Jan Paweł -> ^[J|P][^.]+$
            re_full_name = re.compile(fr'^[{"|".join(a_first_letters)}][^.]+$')

            for j in range(i + 1, n):
                b_surname, b_names = full_names[j][0], full_names[j][1:]

                if a_surname == b_surname \
                        and len(a_names) == len(b_names) \
                        and (all(a_names[k] == b_names[k]  # Jan ~ Jan or J. ~ J.
                                 or (re_full_name.match(a_names[k]) and re_short_name.match(b_names[k]))  # Jan ~ J.
                                 or (re_full_name.match(b_names[k]) and re_short_name.match(a_names[k]))  # J. ~ Jan
                                 for k in range(len(a_names)))):
                    similar.append((i, j))
        except re.error:
            errors.append(full_names[i])
    return similar, errors


def get_node_statistic(authors_df, graph, node_index):
    id = authors_df.index[node_index]
    name = authors_df.loc[id, 'name']
    try:
        in_d, out_d = graph.in_degree(id, weight='weight'), graph.out_degree(id, weight='weight')
    except nx.NetworkXError:
        in_d, out_d = 0, 0
    return {'id': id, 'name': name, 'in_d': in_d, 'out_d': out_d}


def main():
    ex_nodes = get_excessive_nodes(NODES_FILE, INPUT_GRAPH_PATH)
    # clean authors csv
    authors_df = pd.read_csv(NODES_FILE, index_col='id')
    authors_df = authors_df.drop(ex_nodes)
    authors_df.to_csv(OUTPUT_NODES_PATH)


def test_main():
    authors_df = pd.read_csv(OUTPUT_NODES_PATH, index_col='id')
    similar, _ = find_clones(authors_df['name'].values)
    assert len(similar) == 0


if __name__ == '__main__':
    main()
    # test_main()

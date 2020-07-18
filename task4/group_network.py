from pathlib import Path

import infomap
import networkx as nx
from networkx.algorithms import community
import pandas as pd


from build_graph import GRAPH_DIR

OUTPUT_COLORS_FILE = Path('data/colors/pcm/overlaps.csv')


def infomap_usage():
    glabels = pd.read_csv("data/giant/giant_no_copies.csv", sep=',')

    im = infomap.Infomap("--two-level --directed")

    id_dict = dict()
    idx = 1

    for index, row in glabels.iterrows():
        source = row["source"]
        target = row["target"]
        weight = row["weight"]

        if source in id_dict:
            source_id = id_dict[source]
        else:
            id_dict[source] = idx
            idx += 1

            source_id = id_dict[source]

        if target in id_dict:
            target_id = id_dict[target]
        else:
            id_dict[target] = idx
            idx += 1
            target_id = id_dict[target]

        im.addLink(source_id, target_id, float(weight))

    im.run()

    print(
        f"Found {im.num_top_modules} modules with codelength: {im.codelength}")

    print("Result")
    print("\n#node module")
    for node in im.tree:
        if node.is_leaf:
            print(node.node_id, node.module_id)

    reversed_dictionary = {value: key for (key, value) in id_dict.items()}

    modules = pd.read_csv("data/graph/groups_with_fake_ids.csv", sep=" ")
    modules = modules.replace({"#node": reversed_dictionary})
    modules.to_csv("groups.csv", sep=";", index=False)


def clique_communities():
    graph_df = pd.read_csv(GRAPH_DIR / 'graph_name_without_copies.csv', sep=';')
    graph = nx.from_pandas_edgelist(graph_df, edge_attr='weight', create_using=nx.DiGraph())
    graph = graph.to_undirected(reciprocal=True)
    # edge_list = nx.to_pandas_edgelist(graph)
    # edge_list.to_csv(GRAPH_DIR / 'graph_name_without_copies_undirected.csv', sep=';', index=None)

    clusters = list(community.k_clique_communities(graph, 9))
    colors = pd.DataFrame(columns=['Id', 'color'])
    for c in clusters:
        for node in c:
            # colors = colors.append(
            #     {'node': node, 'color': sum([node in cl for cl in clusters])},
            #     ignore_index=True)
            color = clusters.index(c)
            if sum([node in cl for cl in clusters]) > 1:
                color = len(clusters)
            colors = colors.append(
                {'Id': node, 'color': color},
                ignore_index=True)

    colors.to_csv(OUTPUT_COLORS_FILE, index=False)


if __name__ == '__main__':
    infomap_usage()
    clique_communities()

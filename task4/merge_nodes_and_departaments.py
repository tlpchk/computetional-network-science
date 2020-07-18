import os

import pandas as pd

if __name__ == '__main__':
    nodes = pd.read_csv("data/nodes.csv")
    names_and_deps = pd.read_csv("data/names_and_departaments.csv")
    wydzialy = list()
    katedry = list()

    for idx, employee in nodes.iterrows():
        if idx % 100 == 0:
            print(idx)

        name = employee["name"]

        name_split = name.split(" ")

        inserted = False
        for idx2, name_dep in names_and_deps.iterrows():

            first_name = name_dep["first_name"]
            last_name = name_dep["last_name"]
            wydzial = name_dep["wydzial"]
            katedra = name_dep["katedra"]

            last_name_nodes = name_split[0]
            first_name_nodes = name_split[1]
            if last_name == last_name_nodes and (first_name_nodes == first_name or first_name_nodes == first_name_nodes[0]+'.'):
                inserted = True
                wydzialy.append(wydzial)
                katedry.append(katedra)
                break

        if not inserted:
            wydzialy.append("Unknown")
            katedry.append("Unknown")


    numbers_of_citations = list()

    for idx, employee in nodes.iterrows():
        number_of_all_authors_citations = 0
        employee_id = employee["id"]

        file_path = os.path.join("data/citations", f"{employee_id}.csv")
        if os.path.isfile(file_path) and os.stat(file_path).st_size !=0:
            citations = pd.read_csv(file_path)
            if "Author(s) ID" in citations:
                for idx2, paper in citations.iterrows():
                    if type(paper["Author(s) ID"]) != float:
                        number_of_all_authors_citations += len(paper["Author(s) ID"].split(";"))

        numbers_of_citations.append(number_of_all_authors_citations)


    nodes.insert(3,"citation_count",numbers_of_citations, True)
    nodes.insert(4,"Wydzial",wydzialy, True)
    nodes.insert(5,"Katedra",katedry, True)

    nodes.to_csv("data/nodes_deps.csv",sep=',', index=False)
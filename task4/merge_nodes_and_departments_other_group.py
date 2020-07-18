import pandas as pd
import re

if __name__ == '__main__':
    nodes = pd.read_csv("data/nodes_deps_with_other_group.csv")
    nodes_other_group = pd.read_csv("data/nodes_original_with_authors_OTHER_GROUP.csv")

    i=0
    em_count = 0
    for idx, employee in nodes.iterrows():
        if idx % 100 == 0:
            print(idx)
            print(f"Inserted: {i}, searched: {em_count}")

        if employee["Wydzial"] == "Unknown":
            name = employee["name"]
            em_count +=1

            name = re.sub('[^A-Za-z0-9 ]+ ', '', name)
            name = re.sub('[A-Z]+', lambda m: m.group(0).lower(), name)
            name = re.sub('[ą]','a',name)
            name = re.sub('[ć]','c',name)
            name = re.sub('[ę]','e',name)
            name = re.sub('[ł]','l',name)
            name = re.sub('[ń]','n',name)
            name = re.sub('[ó]','o',name)
            name = re.sub('[ś]','s',name)
            name = re.sub('[ź]','z',name)
            name = re.sub('[ż]','z',name)
            name = re.sub('[Ą]','a',name)
            name = re.sub('[Ć]','c',name)
            name = re.sub('[Ę]','e',name)
            name = re.sub('[Ł]','l',name)
            name = re.sub('[Ń]','n',name)
            name = re.sub('[Ó]','o',name)
            name = re.sub('[Ś]','s',name)
            name = re.sub('[Ź]','z',name)
            name = re.sub('[Ż]','z',name)

            name_split = name.split(" ")
            # print(name_split)

            inserted = False

            for idx2, employee2 in nodes_other_group.iterrows():
                if inserted:
                    break

                name2 = employee2["label"]
                department = employee2["department"]

                name2 = re.sub('[^A-Za-z0-9 ]', '', name2)
                name2 = re.sub('[A-Z]+', lambda m: m.group(0).lower(), name2)
                name2 = re.sub('[ą]','a',name2)
                name2 = re.sub('[ć]','c',name2)
                name2 = re.sub('[ę]','e',name2)
                name2 = re.sub('[ł]','l',name2)
                name2 = re.sub('[ń]','n',name2)
                name2 = re.sub('[ó]','o',name2)
                name2 = re.sub('[ś]','s',name2)
                name2 = re.sub('[ź]','z',name2)
                name2 = re.sub('[ż]','z',name2)
                name2 = re.sub('[Ą]','a',name2)
                name2 = re.sub('[Ć]','c',name2)
                name2 = re.sub('[Ę]','e',name2)
                name2 = re.sub('[Ł]','l',name2)
                name2 = re.sub('[Ń]','n',name2)
                name2 = re.sub('[Ó]','o',name2)
                name2 = re.sub('[Ś]','s',name2)
                name2 = re.sub('[Ź]','z',name2)
                name2 = re.sub('[Ż]','z',name2)


                name_split2 = name2.split(" ")

                if (len(name_split2) >= 2 and len(name_split) >= 2 and name_split2[1] == name_split[0] and name_split2[0] ==
                    name_split[1]) or \
                        (len(name_split2) >= 2 and len(name_split) >= 2 and name_split2[1] == name_split[0] and len(name_split[1]) >0 and len(name_split2[0]) >0 and
                         name_split2[0][0] == name_split[1][0]) or \
                        (len(name_split2) >= 3 and len(name_split) >= 2 and name_split[0] == name_split2[2] and name_split2[
                            0] == name_split[1]) or \
                        (len(name_split2) >= 3 and len(name_split) >= 2 and name_split[0] == name_split2[2]and len(name_split[1]) >0 and len(name_split2[0]) >0 and
                         name_split[1][0] == name_split2[0][0]) or \
                        (len(name_split2) ==3 and len(name_split)>=2 and ((name_split[0].startswith(name_split2[2])and len(name_split2[2])>1) or (name_split2[2].startswith(name_split[0]) and len(name_split[0])>1)) and
                         name_split2[0] == name_split[1])or \
                        (len(name_split2) == 2 and len(name_split) >= 2 and (
                                name_split[0].startswith(name_split2[1]) or name_split2[1].startswith(
                            name_split[0])) and name_split2[0] == name_split[1]):
                    employee["Wydzial"] = department
                    if department == "Nieznane":
                        employee["Wydzial"] = "Unknown"
                    nodes.loc[idx] = employee
                    inserted = True
                    i+=1

    nodes.to_csv("data/nodes_deps_with_other_group.csv", sep=',', index=False)

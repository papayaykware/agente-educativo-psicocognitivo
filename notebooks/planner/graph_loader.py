import yaml
import networkx as nx

def load_graph():
    with open("data/curriculum_graph.yaml") as f:
        data = yaml.safe_load(f)

    G = nx.DiGraph()
    for node in data["concepts"]:
        G.add_node(node["id"])
        for prereq in node["prerequisites"]:
            G.add_edge(prereq, node["id"])
    return G

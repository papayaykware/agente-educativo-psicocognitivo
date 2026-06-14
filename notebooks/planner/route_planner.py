import networkx as nx
from .graph_loader import load_graph

def plan_route(start: str, goal: str):
    G = load_graph()
    return nx.shortest_path(G, start, goal)

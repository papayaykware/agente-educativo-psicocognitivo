from fastapi import APIRouter
from planner.graph_loader import load_graph

router = APIRouter()

@router.get("/graph")
def get_graph():
    graph = load_graph()
    return {"nodes": list(graph.nodes), "edges": list(graph.edges)}

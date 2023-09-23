import random

from networkx import MultiDiGraph

def generate_random_multidigraph(  # type: ignore[no-any-unimported]
    num_nodes: int, num_edges: int, node_types: list, edge_types: list
) -> MultiDiGraph:
    """
    Generate a random MultiDiGraph with given node and edge types.

    Parameters:
    - num_nodes: Number of nodes in the graph.
    - num_edges: Number of edges in the graph.
    - node_types: List of possible node types.
    - edge_types: List of possible edge types.

    Returns:
    - A MultiDiGraph with random edges and node/edge types.
    """
    nx_g = MultiDiGraph()

    # Add nodes with random types
    for i in range(num_nodes):
        ntype = random.choice(node_types)
        nx_g.add_node(i, ntype=ntype)

    # Add edges with random types
    for _ in range(num_edges):
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)
        while u == v:  # Ensure source and target nodes are different
            v = random.randint(0, num_nodes - 1)
        etype = random.choice(edge_types)
        nx_g.add_edge(u, v, etype=etype)

    return nx_g


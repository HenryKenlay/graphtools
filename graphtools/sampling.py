# AUTOGENERATED! DO NOT EDIT! File to edit: 01_sampling.ipynb (unless otherwise specified).

__all__ = ['sample_nodes', 'sample_node']

# Cell
def sample_nodes(G, num_nodes=1):
    "Uniformly samples num_nodes nodes"
    nodes = G.nodes()
    return np.random.choice(list(nodes), num_nodes, replace=False)

def sample_node(G):
    "Uniformly samples a single node"
    nodes = G.nodes()
    return np.random.choice(list(nodes))
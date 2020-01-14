# AUTOGENERATED! DO NOT EDIT! File to edit: 04_plotting.ipynb (unless otherwise specified).

__all__ = ['highlight_edges', 'heatmap', 'sfdp_layout', 'neato_layout', 'fdp_layout', 'get_graph_tool_graph',
           'get_networkx_graph', 'nxpos_to_graphtpos']

# Cell
from nbdev.showdoc import *
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns
import graph_tool as gt
import pyintergraph

# Cell
def highlight_edges(G, edges, ax, pos, node_size=300):
    "Draws the graph G with edges in `edges` drawn in red"
    nx.draw_networkx_nodes(G, pos=pos, node_size=10, ax=ax)
    nx.draw_networkx_edges(G, pos=pos, edgelist=set(G.edges()) - set(edges), ax=ax)
    nx.draw_networkx_edges(G, pos=pos, edgelist=edges, ax=ax, edge_color='red')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    return ax

# Cell
def heatmap(df, x, y, hue, xbins=15, ybins=15, xlim=None, ylim=None, bin_numbers=False, bin_cutoff=1, rounding=3, ax=None, vmin=None, vmax=None, cbar=True):
    """
        Plots a heatmap binning the df data based on columns x and y
    """
    df = df.copy()
    if ax is None:
        fig, ax = plt.subplots()
    if xlim is None:
        xlim = (df[x].min(), df[x].max())
    if ylim is None:
        ylim = (df[y].min(), df[y].max())

    xstep = (xlim[1]-xlim[0])/xbins
    xbins = np.arange(xlim[0], xlim[1]+xstep, xstep)
    df[x] = pd.cut(df[x], xbins).map(lambda x : x.mid)

    ystep = (ylim[1]-ylim[0])/ybins
    ybins = np.arange(ylim[0], ylim[1]+ystep, ystep)
    df[y] = pd.cut(df[y], ybins).map(lambda y : y.mid)

    heatmap_data = df.groupby([x, y]).mean()[hue].reset_index()
    heatmap_data = heatmap_data.pivot(y, x, hue)

    heatmap_count = df.groupby([x, y]).count()[hue].reset_index()
    heatmap_count = heatmap_count.pivot(y, x, hue)
    mask = heatmap_count < bin_cutoff
    heatmap_count = heatmap_count.fillna(0).astype(int)
    annot = heatmap_count if bin_numbers else None

    sns.heatmap(heatmap_data, ax = ax, cmap="YlGnBu", mask=mask, annot=annot, vmin=vmin, vmax=vmax, cbar = cbar, fmt='d')
    ax.set_xticklabels([round(float(item.get_text()), rounding) for item in ax.get_xticklabels()])
    ax.set_yticklabels([round(float(item.get_text()), rounding) for item in ax.get_yticklabels()])
    return ax

# Cell
def sfdp_layout(G):
    G = get_graph_tool_graph(G)
    pos = gt.draw.sfdp_layout(G)
    return pos

def neato_layout(G):
    Gnx = get_networkx_graph(G)
    pos = nx.drawing.nx_agraph.graphviz_layout(Gnx, prog='neato')
    return nxpos_to_graphtpos(G, pos)

def fdp_layout(G):
    Gnx = get_networkx_graph(G)
    pos = nx.drawing.nx_agraph.graphviz_layout(Gnx, prog='fdp')
    return nxpos_to_graphtpos(G, pos)

# Cell

def get_graph_tool_graph(G):
    if 'networkx' in str(type(G)):
        G = pyintergraph.nx2gt(G, labelname="node_label")
    return G

def get_networkx_graph(G):
    if 'graph_tool' in str(type(G)):
        G = pyintergraph.gt2nx(G)
    return G

def nxpos_to_graphtpos(G, nx_pos):
    """
        Takes a graph G (networkx or graph_tool) and a position dictionary and returns a graph_tool graph and VertexPropertyMap for plotting
    """
    G = get_graph_tool_graph(G)
    pos = G.new_vertex_property('vector<double>')
    for i in nx_pos:
        pos[i] = nx_pos[i]
    return pos
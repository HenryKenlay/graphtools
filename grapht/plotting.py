# AUTOGENERATED! DO NOT EDIT! File to edit: 04_plotting.ipynb (unless otherwise specified).

__all__ = ['highlight_edges', 'heatmap']

# Cell
from nbdev.showdoc import *
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns

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
    annot = heatmap_count if bin_numbers else None

    sns.heatmap(heatmap_data, ax = ax, cmap="YlGnBu", mask=mask, annot=annot, vmin=vmin, vmax=vmax, cbar = cbar)
    ax.set_xticklabels([round(float(item.get_text()), rounding) for item in ax.get_xticklabels()])
    ax.set_yticklabels([round(float(item.get_text()), rounding) for item in ax.get_yticklabels()])
    return ax
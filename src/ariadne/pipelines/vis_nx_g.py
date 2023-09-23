from math import log
import networkx as nx
import plotly.graph_objects as go
from networkx import MultiDiGraph
from plotly.graph_objects import Figure

from ariadne.nodes.utils_vis_nx_g import get_distinct_colors


def return_fig_multigraph(  # type: ignore[no-any-unimported]
    nx_g: MultiDiGraph,
) -> Figure:
    """
    Visualize a MultiDiGraph with Plotly, distinguishing multiple edges and indicating edge directions.
    Adjusts element sizes based on the number of nodes and edges and includes a legend.

    Parameters:
    - nx_g: A networkx MultiDiGraph instance.

    Returns:
    - A Plotly figure.
    """
    # Compute the layout positions
    pos = nx.drawing.nx_agraph.graphviz_layout(nx_g, prog="neato")

    # Adjusted scaling factors based on graph size
    num_nodes = len(nx_g.nodes())
    num_edges = len(nx_g.edges())
    
    # Define size bounds
    MIN_NODE_SIZE, MAX_NODE_SIZE = 10, 30
    MIN_EDGE_WIDTH, MAX_EDGE_WIDTH = 1, 5

    # Arbitrary large number for scaling (e.g., assuming the largest graph will have 10,000 nodes/edges)
    MAX_ELEMENTS = 10000

    # Calculate node and edge sizes
    node_size = MIN_NODE_SIZE + (log(num_nodes + 1) - 1) * (MAX_NODE_SIZE - MIN_NODE_SIZE) / (log(MAX_ELEMENTS + 1) - 1)
    edge_width = MIN_EDGE_WIDTH + (log(num_edges + 1) - 1) * (MAX_EDGE_WIDTH - MIN_EDGE_WIDTH) / (log(MAX_ELEMENTS + 1) - 1)
    node_size = min(10, 30000.0 / num_nodes)
    edge_width = min(1, 2800.0 / num_edges)

    # Get unique node and edge types and create color maps
    node_types = set(nx.get_node_attributes(nx_g, "ntype").values())
    edge_types = set(nx.get_edge_attributes(nx_g, "etype").values())
    node_color_map = dict(zip(node_types, get_distinct_colors(len(node_types))))
    edge_color_map = dict(zip(edge_types, get_distinct_colors(len(edge_types))))

    # Create traces for nodes
    node_x = []
    node_y = []
    node_hovertext = []
    node_colors = []
    for node, data in nx_g.nodes(data=True):
        node_x.append(pos[node][0])
        node_y.append(pos[node][1])
        hovertext = "<br>".join(
            [f"{k}: {v}" if len(str(v)) < 25 else f"{k}: ..." for k, v in data.items()]
        )
        node_hovertext.append(hovertext)
        node_colors.append(node_color_map[data["ntype"]])

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        hovertext=node_hovertext,
        marker=dict(color=node_colors, size=node_size),
        name="nodes",
        showlegend=False,
    )

    # Create legend items for node types
    node_legend_traces = [
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(color=color, size=node_size),
            showlegend=True,
            name=f"Node: {ntype}",
            legendgroup=f"Node: {ntype}",
        )
        for ntype, color in node_color_map.items()
    ]

    # Create traces for edges grouped by edge type
    edge_traces = []
    edge_marker_traces = []
    for etype, color in edge_color_map.items():
        edge_x = []
        edge_y = []
        edge_hovertext = []
        edge_marker_x = []
        edge_marker_y = []

        for u, v, key, data in nx_g.edges(keys=True, data=True):
            if data["etype"] == etype:
                x0, y0 = pos[u]
                x1, y1 = pos[v]

                # Calculate offset for curved lines
                offset = 0.1 * key
                ctrl_x, ctrl_y = (x0 + x1) / 2 + offset * (y1 - y0), (
                    y0 + y1
                ) / 2 + offset * (x0 - x1)

                edge_x.extend([x0, ctrl_x, x1, None])
                edge_y.extend([y0, ctrl_y, y1, None])

                hovertext = "<br>".join(
                    [
                        f"{k}: {v}" if len(str(v)) < 25 else f"{k}: ..."
                        for k, v in data.items()
                    ]
                )
                edge_hovertext.append(hovertext)

                # Invisible node positions for hovertext
                edge_marker_x.append(ctrl_x)
                edge_marker_y.append(ctrl_y)

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=edge_width, color=color),
            hoverinfo="none",
            mode="lines",
            name=f"Edge: {etype}",
            legendgroup=f"Edge: {etype}",
        )

        edge_marker_trace = go.Scatter(
            x=edge_marker_x,
            y=edge_marker_y,
            mode="markers",
            hoverinfo="text",
            hovertext=edge_hovertext,
            marker=dict(size=0, opacity=0),
            legendgroup=f"Edge: {etype}",
            showlegend=False,
        )

        edge_traces.append(edge_trace)
        edge_marker_traces.append(edge_marker_trace)

    data = [node_trace] + node_legend_traces + edge_traces + edge_marker_traces

    figure_width = max(1280, 0.6 * nx_g.number_of_nodes())
    figure_height = max(960, 0.4 * nx_g.number_of_nodes())

    fig = go.Figure(
        data=data,
        layout=go.Layout(
            title="MultiDiGraph Visualization",
            titlefont_size=16,
            showlegend=True,
            hovermode="closest",
            margin=dict(b=0, l=0, r=0, t=40),
            width=figure_width,
            height=figure_height,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )

    return fig

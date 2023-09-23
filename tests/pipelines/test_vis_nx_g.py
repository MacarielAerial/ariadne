from networkx import MultiDiGraph

from ariadne.pipelines.vis_nx_g import return_fig_multigraph


def test_vis_nx_g(  # type: ignore[no-any-unimported]
    random_multidigraph: MultiDiGraph,
) -> None:
    fig = return_fig_multigraph(nx_g=random_multidigraph)

    assert fig

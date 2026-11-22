"""Build the curriculum KG and read/write it as node-link JSON.

File format (``data/kg/example_graph.json``, ``data/kg/graph.json``)::

    {"graph": {...}, "nodes": [{"id": ..., "type": ..., ...}],
     "edges": [{"source": ..., "target": ..., "type": ..., ...}]}

Edges are stored in a ``MultiDiGraph`` keyed by their type, so each (source, target, type)
appears at most once.
"""

import json
from collections.abc import Sequence
from pathlib import Path

import networkx as nx

from vimath_rag.schemas import Chunk


def load_graph(path: str | Path) -> nx.MultiDiGraph:
    """Load a node-link JSON graph; rejects duplicate nodes/edges and dangling endpoints."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    graph = nx.MultiDiGraph()
    graph.graph.update(data.get("graph", {}))
    for node in data["nodes"]:
        attrs = dict(node)
        node_id = attrs.pop("id")
        if node_id in graph:
            raise ValueError(f"{path}: duplicate node id {node_id!r}")
        graph.add_node(node_id, **attrs)
    for edge in data["edges"]:
        attrs = dict(edge)
        u, v = attrs.pop("source"), attrs.pop("target")
        for endpoint in (u, v):
            if endpoint not in graph:
                raise ValueError(f"{path}: edge references unknown node {endpoint!r}")
        etype = attrs.get("type")
        if graph.has_edge(u, v, key=etype):
            raise ValueError(f"{path}: duplicate edge {u!r} -[{etype}]-> {v!r}")
        graph.add_edge(u, v, key=etype, **attrs)
    return graph


def save_graph(graph: nx.MultiDiGraph, path: str | Path) -> None:
    """Write ``graph`` in the same node-link JSON format as :func:`load_graph` reads."""
    data = {
        "graph": dict(graph.graph),
        "nodes": [{"id": n, **attrs} for n, attrs in graph.nodes(data=True)],
        "edges": [{"source": u, "target": v, **attrs} for u, v, attrs in graph.edges(data=True)],
    }
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_graph_from_curated(curated_dir: Path) -> nx.MultiDiGraph:
    """Build the KG from ``lessons.csv``, ``concepts.csv`` and ``edges.csv`` (rows with
    ``status=accepted``). TODO(M3)."""
    raise NotImplementedError("TODO(M3): build_graph_from_curated")


def link_chunks_to_concepts(
    graph: nx.MultiDiGraph, chunks: Sequence[Chunk]
) -> dict[str, list[str]]:
    """Map chunk ids to concept ids: alias matches inside the lessons where each concept appears.
    The result fills ``Chunk.concepts``. TODO(M3)."""
    raise NotImplementedError("TODO(M3): link_chunks_to_concepts")

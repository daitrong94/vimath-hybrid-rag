"""Knowledge-graph schema loaded from ``data/kg/schema.yaml``, and graph validation.

The YAML file is the single source of truth for node and edge types (docs/DATA.md, section 6).
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import networkx as nx
import yaml


class KGValidationError(ValueError):
    """Raised when a graph violates the KG schema."""


@dataclass(frozen=True)
class NodeTypeSpec:
    name: str
    required: frozenset[str]
    enums: Mapping[str, frozenset[str]] = field(default_factory=dict)


@dataclass(frozen=True)
class EdgeTypeSpec:
    name: str
    pairs: frozenset[tuple[str, str]]  # allowed (source node type, target node type)
    required: frozenset[str] = frozenset()
    enums: Mapping[str, frozenset[str]] = field(default_factory=dict)
    acyclic: bool = False
    symmetric: bool = False
    non_decreasing: str | None = None  # node attribute that must not decrease along the edge


@dataclass(frozen=True)
class KGSchema:
    node_types: Mapping[str, NodeTypeSpec]
    edge_types: Mapping[str, EdgeTypeSpec]


def _enums(spec: Mapping[str, Any]) -> dict[str, frozenset[str]]:
    return {attr: frozenset(values) for attr, values in (spec.get("enums") or {}).items()}


def load_kg_schema(path: str | Path) -> KGSchema:
    """Parse ``schema.yaml`` into a :class:`KGSchema`."""
    with Path(path).open(encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    node_types = {
        name: NodeTypeSpec(
            name=name, required=frozenset(spec.get("required", [])), enums=_enums(spec)
        )
        for name, spec in raw["node_types"].items()
    }
    edge_types = {
        name: EdgeTypeSpec(
            name=name,
            pairs=frozenset((src, dst) for src, dst in spec["pairs"]),
            required=frozenset(spec.get("required", [])),
            enums=_enums(spec),
            acyclic=bool(spec.get("acyclic", False)),
            symmetric=bool(spec.get("symmetric", False)),
            non_decreasing=spec.get("non_decreasing"),
        )
        for name, spec in raw["edge_types"].items()
    }
    for edge in edge_types.values():
        unknown = {t for pair in edge.pairs for t in pair} - node_types.keys()
        if unknown:
            raise ValueError(
                f"{path}: edge type {edge.name!r} uses unknown node types {sorted(unknown)}"
            )
    return KGSchema(node_types=node_types, edge_types=edge_types)


def _check_enums(
    where: str, attrs: Mapping[str, Any], enums: Mapping[str, frozenset[str]], errors: list[str]
) -> None:
    for attr, allowed in enums.items():
        if attr in attrs and attrs[attr] not in allowed:
            errors.append(f"{where}: {attr}={attrs[attr]!r} not in {sorted(allowed)}")


def validate_graph(graph: nx.MultiDiGraph, schema: KGSchema) -> None:
    """Check node/edge types, required attributes, enums, allowed endpoint types, acyclicity,
    symmetric-edge storage and grade monotonicity. Raises :class:`KGValidationError` listing
    every violation.

    TODO(M3): every concept with ``grade_introduced >= 6`` has exactly one ``introduced`` lesson.
    """
    errors: list[str] = []

    for node, attrs in graph.nodes(data=True):
        node_spec = schema.node_types.get(attrs.get("type"))
        if node_spec is None:
            errors.append(f"node {node!r}: unknown type {attrs.get('type')!r}")
            continue
        missing = node_spec.required - attrs.keys()
        if missing:
            errors.append(f"node {node!r}: missing attributes {sorted(missing)}")
        _check_enums(f"node {node!r}", attrs, node_spec.enums, errors)

    for u, v, attrs in graph.edges(data=True):
        etype = attrs.get("type")
        where = f"edge {u!r} -[{etype}]-> {v!r}"
        edge_spec = schema.edge_types.get(etype)
        if edge_spec is None:
            errors.append(f"{where}: unknown edge type")
            continue
        pair = (graph.nodes[u].get("type"), graph.nodes[v].get("type"))
        if pair not in edge_spec.pairs:
            errors.append(f"{where}: {pair[0]} -> {pair[1]} is not allowed")
        missing = edge_spec.required - attrs.keys()
        if missing:
            errors.append(f"{where}: missing attributes {sorted(missing)}")
        _check_enums(where, attrs, edge_spec.enums, errors)
        if edge_spec.non_decreasing:
            a = graph.nodes[u].get(edge_spec.non_decreasing)
            b = graph.nodes[v].get(edge_spec.non_decreasing)
            if a is not None and b is not None and a > b:
                errors.append(f"{where}: {edge_spec.non_decreasing} decreases ({a} > {b})")

    for edge_spec in schema.edge_types.values():
        edges = [(u, v) for u, v, t in graph.edges(data="type") if t == edge_spec.name]
        if edge_spec.acyclic:
            sub = nx.DiGraph(edges)
            if not nx.is_directed_acyclic_graph(sub):
                errors.append(f"{edge_spec.name}: cycle {nx.find_cycle(sub)}")
        if edge_spec.symmetric:
            present = set(edges)
            both = sorted({tuple(sorted(e)) for e in present if (e[1], e[0]) in present})
            if both:
                errors.append(f"{edge_spec.name}: symmetric edges stored in both directions {both}")

    if errors:
        raise KGValidationError(f"{len(errors)} KG schema violation(s):\n- " + "\n- ".join(errors))

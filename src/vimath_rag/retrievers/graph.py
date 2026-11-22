"""Graph retrieval over the curriculum knowledge graph (NetworkX).

Pipeline (``configs/retrievers.yaml: graph``):
1. Concept linking: longest match of concept names/aliases in the normalized question;
   fallback: top-m concepts by embedding similarity of their names.
2. Intent: prerequisite cues ("trước khi", "cần biết", ...) mean walking ``prerequisite_of``
   edges backwards from the linked concept.
3. Expansion: personalized PageRank seeded with the linked concepts (edge-type weights), or BFS
   up to ``max_hops``. The PPR idea follows HippoRAG (Gutiérrez et al., 2024).
4. Concept -> chunks: chunks tagged with the concept, or chunks of the lesson that introduces it,
   weighted by chunk type (definition/theorem/formula > example > explanation > exercise).
5. Grade filter, top-k.
"""

from collections.abc import Mapping, Sequence
from typing import Literal

import networkx as nx

from vimath_rag.schemas import Chunk, RetrievedChunk

Expansion = Literal["ppr", "bfs"]


class GraphRetriever:
    """Retrieve chunks through concepts of the curriculum KG."""

    name = "graph"

    def __init__(
        self,
        graph: nx.MultiDiGraph,
        chunks: Sequence[Chunk],
        *,
        expansion: Expansion = "ppr",
        max_hops: int = 2,
        ppr_alpha: float = 0.85,
        edge_weights: Mapping[str, float] | None = None,
        type_weights: Mapping[str, float] | None = None,
        prerequisite_cues: Sequence[str] = (),
    ) -> None:
        self.graph = graph
        self.chunks = chunks
        self.expansion = expansion
        self.max_hops = max_hops
        self.ppr_alpha = ppr_alpha
        self.edge_weights = dict(edge_weights or {})
        self.type_weights = dict(type_weights or {})
        self.prerequisite_cues = tuple(prerequisite_cues)

    def link_concepts(self, question: str) -> list[tuple[str, float]]:
        """Concept ids mentioned in ``question`` with a confidence score. TODO(M3)."""
        raise NotImplementedError("TODO(M3): GraphRetriever.link_concepts")

    def retrieve(self, query: str, k: int = 10, grade: int | None = None) -> list[RetrievedChunk]:
        """Link concepts, expand over the KG, map concepts to chunks, filter, rank. TODO(M3)."""
        raise NotImplementedError("TODO(M3): GraphRetriever.retrieve")

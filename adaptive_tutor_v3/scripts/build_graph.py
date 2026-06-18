from __future__ import annotations

from config import settings
from knowledge_graph.loader import load_graph_from_topics


def main() -> None:
    graph = load_graph_from_topics(settings.data_dir / "topics")
    print(f"Loaded {len(graph.nodes)} concepts.")


if __name__ == "__main__":
    main()

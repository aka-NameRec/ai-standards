#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = ["chromadb>=1.1,<2"]
# ///
"""Freshness-gated Chroma code index for a project.

Managed by ai-standards. Generalized from a battle-tested reference implementation.
Lives at ``<project>/.ai-standards/scripts/code_index.py``; configuration is read
from ``<project>/.ai-standards/code-index.toml``.

Design notes (encoded to avoid re-discovering expensive setup traps):
- Indexing is incremental by per-file SHA-256 content hash.
- The manifest is saved atomically (tmp-file + replace) so an interrupted build
  resumes without re-embedding finished files.
- Embeddings are upserted across file boundaries in batches, not one upsert per
  source file, to avoid the per-upsert startup-cost bottleneck.
- Queries refresh first and block on a refresh failure, so retrieval never runs
  against a stale index.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


SCRIPT = Path(__file__).resolve()
WORKSPACE = SCRIPT.parents[2]
CONFIG_PATH = WORKSPACE / ".ai-standards" / "code-index.toml"


@dataclass(frozen=True)
class Settings:
    raw: dict[str, Any]
    workspace: Path
    chroma_dir: Path
    manifest: Path

    @classmethod
    def load(cls) -> "Settings":
        raw = tomllib.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        config_dir = CONFIG_PATH.parent
        workspace = (config_dir / raw["workspace"]).resolve()
        return cls(
            raw=raw,
            workspace=workspace,
            chroma_dir=(workspace / raw["chroma_dir"]).resolve(),
            manifest=(workspace / raw["manifest"]).resolve(),
        )


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def batched(items: list[Any], size: int = 32) -> Iterable[list[Any]]:
    for start in range(0, len(items), size):
        yield items[start : start + size]


class CodeIndex:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.settings.chroma_dir.mkdir(parents=True, exist_ok=True)
        self.settings.manifest.parent.mkdir(parents=True, exist_ok=True)
        self.manifest = self._load_manifest()

    def _load_manifest(self) -> dict[str, Any]:
        if not self.settings.manifest.exists():
            return {"version": 1, "collections": {}}
        return json.loads(self.settings.manifest.read_text(encoding="utf-8"))

    def _save_manifest(self) -> None:
        temporary = self.settings.manifest.with_suffix(".tmp")
        temporary.write_text(
            json.dumps(self.manifest, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        temporary.replace(self.settings.manifest)

    def _collection_configs(self, requested: str | None) -> list[dict[str, Any]]:
        configs = self.settings.raw["collection"]
        if requested is None:
            return configs
        selected = [item for item in configs if item["name"] == requested]
        if not selected:
            names = ", ".join(item["name"] for item in configs)
            raise SystemExit(f"Unknown collection {requested!r}; expected one of: {names}")
        return selected

    def _excluded(self, relative: str) -> bool:
        return any(
            fnmatch.fnmatch(relative, pattern)
            for pattern in self.settings.raw["exclude_globs"]
        )

    def _eligible_files(self, config: dict[str, Any]) -> dict[str, Path]:
        extensions = set(self.settings.raw["include_extensions"])
        maximum = int(self.settings.raw["max_file_bytes"])
        result: dict[str, Path] = {}
        ignored_dirs = {
            ".git", ".idea", ".next", ".venv", "build", "coverage", "dist",
            "generated", "graphify-out", "node_modules", "target", "vendor",
            "staticfiles", "context_portal", ".ai-standards", ".basic-memory",
        }
        for configured_root in config["roots"]:
            root = self.settings.workspace / configured_root
            if not root.exists():
                continue
            for path in root.rglob("*"):
                if not path.is_file() or any(part in ignored_dirs for part in path.parts):
                    continue
                relative = path.relative_to(self.settings.workspace).as_posix()
                if path.suffix.lower() not in extensions or self._excluded(relative):
                    continue
                try:
                    if path.stat().st_size > maximum:
                        continue
                except OSError:
                    continue
                result[relative] = path
        return result

    def _chunks(self, source: str, text: str) -> list[dict[str, Any]]:
        lines = text.splitlines()
        size = int(self.settings.raw["chunk_lines"])
        overlap = int(self.settings.raw["chunk_overlap"])
        step = max(1, size - overlap)
        chunks: list[dict[str, Any]] = []
        for start in range(0, max(1, len(lines)), step):
            selected = lines[start : start + size]
            if not selected and chunks:
                break
            document = "\n".join(selected).strip()
            if not document:
                continue
            digest = sha256(f"{source}:{start}:{document}".encode())
            chunks.append(
                {
                    "id": digest,
                    "document": document,
                    "metadata": {
                        "source": source,
                        "extension": Path(source).suffix.lower(),
                        "start_line": start + 1,
                        "end_line": min(len(lines), start + size),
                        "content_hash": sha256(document.encode()),
                    },
                }
            )
            if start + size >= len(lines):
                break
        return chunks

    def refresh(self, requested: str | None = None) -> None:
        import chromadb

        client = chromadb.PersistentClient(path=str(self.settings.chroma_dir))
        for config in self._collection_configs(requested):
            name = config["name"]
            collection = client.get_or_create_collection(name=name)
            state = self.manifest["collections"].setdefault(name, {})
            files = self._eligible_files(config)
            current_sources = set(files)
            removed = sorted(set(state) - current_sources)
            changed = 0
            unchanged = 0
            pending: list[tuple[str, str, list[dict[str, Any]]]] = []

            for source in removed:
                ids = state[source].get("ids", [])
                if ids:
                    collection.delete(ids=ids)
                del state[source]

            for source, path in sorted(files.items()):
                try:
                    data = path.read_bytes()
                    content_hash = sha256(data)
                    if state.get(source, {}).get("hash") == content_hash:
                        unchanged += 1
                        continue
                    text = data.decode("utf-8")
                except (OSError, UnicodeDecodeError):
                    continue

                chunks = self._chunks(source, text)
                pending.append((source, content_hash, chunks))

            # Embed across file boundaries. Chroma's embedding model has a fixed
            # startup cost per upsert; one upsert per source file makes an initial
            # workspace build unnecessarily slow.
            for file_batch in batched(pending, 100):
                all_chunks: list[dict[str, Any]] = []
                for source, _, chunks in file_batch:
                    old_ids = state.get(source, {}).get("ids", [])
                    if old_ids:
                        collection.delete(ids=old_ids)
                    all_chunks.extend(chunks)
                for chunk_batch in batched(all_chunks, 128):
                    collection.upsert(
                        ids=[item["id"] for item in chunk_batch],
                        documents=[item["document"] for item in chunk_batch],
                        metadatas=[item["metadata"] for item in chunk_batch],
                    )
                for source, content_hash, chunks in file_batch:
                    state[source] = {
                        "hash": content_hash,
                        "ids": [item["id"] for item in chunks],
                    }
                    changed += 1
                self._save_manifest()

            self._save_manifest()
            print(
                f"{name}: fresh; changed={changed}, removed={len(removed)}, "
                f"unchanged={unchanged}, records={collection.count()}"
            )

    def query(self, question: str, requested: str | None, limit: int) -> None:
        import chromadb

        self.refresh(requested)
        client = chromadb.PersistentClient(path=str(self.settings.chroma_dir))
        rows: list[tuple[float, str, dict[str, Any], str]] = []
        for config in self._collection_configs(requested):
            collection = client.get_collection(name=config["name"])
            result = collection.query(query_texts=[question], n_results=limit)
            documents = result.get("documents", [[]])[0]
            metadatas = result.get("metadatas", [[]])[0]
            distances = result.get("distances", [[]])[0]
            for distance, metadata, document in zip(distances, metadatas, documents):
                rows.append((float(distance), config["name"], metadata, document))

        for rank, (distance, name, metadata, document) in enumerate(sorted(rows)[:limit], 1):
            excerpt = document[:1200].replace("\x00", "")
            print(
                f"\n[{rank}] distance={distance:.4f} collection={name} "
                f"source={metadata['source']}:{metadata['start_line']}-{metadata['end_line']}"
            )
            print(excerpt)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)

    refresh = commands.add_parser("refresh", help="Refresh one or all Chroma collections.")
    refresh.add_argument("name", nargs="?", help="Optional collection name.")

    code_query = commands.add_parser("code-query", help="Refresh, then semantic-search the code.")
    code_query.add_argument("question")
    code_query.add_argument("--collection")
    code_query.add_argument("--limit", type=int, default=10)
    return result


def main() -> None:
    args = parser().parse_args()
    settings = Settings.load()
    if args.command == "refresh":
        CodeIndex(settings).refresh(args.name)
    elif args.command == "code-query":
        CodeIndex(settings).query(args.question, args.collection, args.limit)


if __name__ == "__main__":
    main()

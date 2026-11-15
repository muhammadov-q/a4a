"""Do the distinct tool candidates saturate as repositories are added?

    uv run --group analysis repo2tools corpus-saturation --base-url http://127.0.0.1:18002/v1 --model qwen3-embedding

1. The candidates of every scanned repository at the three levels (`corpus.granularity`).
2. One vector per candidate text, from a text-embedding model at an OpenAI-compatible endpoint. The vectors
   are kept in out/corpus/embeddings/, so the rest can be repeated without the model.
3. Groups of candidates that do the same thing: repositories are added one by one, and a candidate joins the
   most similar group seen so far if its cosine similarity to that group's first member is at least the
   threshold; otherwise it starts a new group. The first member stands for the group, so a group cannot drift.
4. The number of groups after k repositories, averaged over random orders of the repositories, for several
   thresholds, for all candidates and for those the repository's own documentation uses.

A curve that keeps growing in step with the candidates means every repository brings new tools; a curve that
bends means later repositories mostly repeat earlier ones. The bend is summarised by the exponent b in
groups = a * candidates^b (1 = no repetition, smaller = saturating).

Writes out/corpus/saturation.json and saturation.md, and saturation_pairs.md: pairs of candidates from
different repositories at several similarities, to judge by reading which threshold means "the same tool".
"""

import argparse
import json
import random
from pathlib import Path

from repo2tools.corpus.granularity import tool_candidates
from repo2tools.paths import REPO_ROOT

OUT = REPO_ROOT / "out" / "corpus"
LEVELS = ("low", "medium", "high")
DIMENSIONS = 1024  # the leading part of the vector; the embedding models used here are trained to allow this
BANDS = ((0.95, 1.01), (0.90, 0.95), (0.85, 0.90), (0.80, 0.85), (0.75, 0.80), (0.70, 0.75), (0.60, 0.70))


def load_candidates(scans: Path) -> dict[str, list[dict]]:
    """Repository folder name -> its candidates, for every repository with saved scans."""
    found = {}
    for folder in sorted(p for p in scans.iterdir() if (p / "api.json").is_file() and (p / "usage.json").is_file()):
        found[folder.name] = tool_candidates(json.loads((folder / "api.json").read_text()), json.loads((folder / "usage.json").read_text()))
    return found


def embed(texts: list[str], client, model: str, batch: int = 64):
    """Unit vectors, one per text, in order."""
    import numpy as np

    rows = []
    for start in range(0, len(texts), batch):
        reply = client.embeddings.create(model=model, input=[t[:2000] or " " for t in texts[start:start + batch]])
        rows += [item.embedding[:DIMENSIONS] for item in sorted(reply.data, key=lambda item: item.index)]
    vectors = np.asarray(rows, dtype=np.float32)
    return vectors / np.maximum(np.linalg.norm(vectors, axis=1, keepdims=True), 1e-12)


def count_groups(by_repo: list, threshold: float) -> list[int]:
    """Number of groups after each repository, in the given order. `by_repo`: one array of unit vectors per repository."""
    import numpy as np

    total = sum(len(v) for v in by_repo)
    width = next((v.shape[1] for v in by_repo if len(v)), 1)
    leaders = np.zeros((total, width), dtype=np.float32)
    n, counts = 0, []
    for vectors in by_repo:
        if len(vectors):
            new = np.ones(len(vectors), dtype=bool) if n == 0 else (vectors @ leaders[:n].T).max(axis=1) < threshold
            first = n
            for row in vectors[new]:  # candidates of this repository can repeat each other too
                if n == first or float((leaders[first:n] @ row).max()) < threshold:
                    leaders[n] = row
                    n += 1
        counts.append(n)
    return counts


def exponent(candidates: list[int], groups: list[float]) -> float | None:
    """b in groups = a * candidates^b, by least squares on the logarithms. None with fewer than three points."""
    import numpy as np

    points = [(c, g) for c, g in zip(candidates, groups) if c > 0 and g > 0]
    if len(points) < 3 or len({c for c, _ in points}) < 3:
        return None
    x, y = np.log([c for c, _ in points]), np.log([g for _, g in points])
    return round(float(np.polyfit(x, y, 1)[0]), 3)


def curve(by_repo: list, threshold: float, orders: int, seed: int = 0) -> dict:
    """Groups after k repositories, over random orders of the repositories: mean, smallest and largest, and the exponent."""
    import numpy as np

    rng = random.Random(seed)
    runs, sizes = [], []
    for _ in range(orders):
        order = list(range(len(by_repo)))
        rng.shuffle(order)
        runs.append(count_groups([by_repo[i] for i in order], threshold))
        sizes.append(np.cumsum([len(by_repo[i]) for i in order]).tolist())
    runs_array, sizes_array = np.asarray(runs, dtype=float), np.asarray(sizes, dtype=float)
    mean, mean_size = runs_array.mean(axis=0), sizes_array.mean(axis=0)
    tail = max(1, len(by_repo) // 10)  # the last tenth of the repositories
    new_late = (runs_array[:, -1] - runs_array[:, -tail - 1]) / np.maximum(sizes_array[:, -1] - sizes_array[:, -tail - 1], 1) if len(by_repo) > tail else None
    return {"groups": [round(v, 1) for v in mean.tolist()], "lowest": runs_array.min(axis=0).astype(int).tolist(), "highest": runs_array.max(axis=0).astype(int).tolist(),
            "candidates": [round(v, 1) for v in mean_size.tolist()], "exponent": exponent(mean_size.tolist(), mean.tolist()),
            "new_in_last_tenth": round(float(new_late.mean()), 3) if new_late is not None else None}


def similar_pairs(ids: list[str], texts: list[str], repos: list[str], vectors, per_band: int = 10, sample: int = 3000, seed: int = 0) -> dict[str, list[dict]]:
    """For a sample of candidates, the most similar candidate of another repository; a few such pairs per band of similarity."""
    import numpy as np

    rng = random.Random(seed)
    picked = rng.sample(range(len(ids)), min(sample, len(ids)))
    repo_index = np.asarray([hash(r) for r in repos])
    pairs = []
    for start in range(0, len(picked), 500):
        rows = picked[start:start + 500]
        scores = vectors[rows] @ vectors.T
        scores[repo_index[rows][:, None] == repo_index[None, :]] = -1.0  # only other repositories
        best = scores.argmax(axis=1)
        pairs += [(float(scores[k, j]), i, int(j)) for k, (i, j) in enumerate(zip(rows, best))]
    out: dict[str, list[dict]] = {}
    for low, high in BANDS:
        inside = [p for p in pairs if low <= p[0] < high]
        rng.shuffle(inside)
        out[f"{low:.2f} to {min(high, 1.0):.2f}"] = [{"similarity": round(score, 3), "a": f"[{repos[i]}] {texts[i][:300]}", "b": f"[{repos[j]}] {texts[j][:300]}"} for score, i, j in inside[:per_band]]
    return out


def report(result: dict) -> str:
    marks = [k for k in (1, 5, 10, 20, 40, 60, 80, 100, 200, 500, 1000) if k <= result["repositories"]]
    if marks[-1] != result["repositories"]:
        marks.append(result["repositories"])
    lines = ["# Do the distinct tool candidates saturate?", "",
             f"{result['repositories']} repositories, embedding model `{result['model']}`, {result['orders']} random orders of the repositories. "
             "A candidate joins a group if its similarity to the group's first member is at least the threshold.", "",
             "Exponent: b in groups = a * candidates^b. 1 means no repetition; smaller means later repositories repeat earlier ones. "
             "New in the last tenth: of the candidates the last tenth of the repositories bring, the share that starts a new group.", ""]
    for subset, title in (("all", "All candidates"), ("used_in_docs", "Candidates the repository's own documentation uses")):
        lines += [f"## {title}", "", "| Level | Threshold | Candidates | Groups | Groups per candidate | Exponent | New in the last tenth | " + " | ".join(f"k={k}" for k in marks) + " |",
                  "| --- | --- | --- | --- | --- | --- | --- | " + " | ".join("---" for _ in marks) + " |"]
        for level in LEVELS:
            for threshold, c in sorted(result["curves"][subset][level].items()):
                total, groups = c["candidates"][-1], c["groups"][-1]
                lines.append(f"| {level} | {threshold} | {total:,.0f} | {groups:,.0f} | {groups / max(total, 1):.2f} | {c['exponent']} | "
                             f"{c['new_in_last_tenth']:.0%} | " + " | ".join(f"{c['groups'][k - 1]:,.0f}" for k in marks) + " |")
        lines.append("")
    return "\n".join(lines)


def pairs_report(pairs: dict) -> str:
    lines = ["# Pairs of candidates from different repositories, by similarity", "",
             "For choosing the threshold: read the pairs and mark from which similarity on two candidates are the same tool.", ""]
    for level, bands in pairs.items():
        lines += [f"## {level}", ""]
        for band, rows in bands.items():
            lines += [f"### Similarity {band}", ""]
            for row in rows:
                lines += [f"- **{row['similarity']}**", f"  - {row['a']}".replace("\n", " "), f"  - {row['b']}".replace("\n", " ")]
            lines.append("")
    return "\n".join(lines)


def main() -> None:
    import numpy as np
    from openai import OpenAI

    from repo2tools.synthesis.pipeline import api_key_for

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base-url", help="OpenAI-compatible endpoint with an embedding model; not needed if the vectors are already saved")
    parser.add_argument("--model", required=True, help="embedding model name at the endpoint; also names the folder of saved vectors")
    parser.add_argument("--thresholds", type=float, nargs="+", default=[0.80, 0.85, 0.90])
    parser.add_argument("--orders", type=int, default=10)
    parser.add_argument("--scans", type=Path, default=OUT / "scans")
    args = parser.parse_args()

    by_repo = load_candidates(args.scans)
    cache = OUT / "embeddings" / args.model
    cache.mkdir(parents=True, exist_ok=True)
    client = OpenAI(base_url=args.base_url, api_key=api_key_for(args.base_url)) if args.base_url else None
    result = {"model": args.model, "repositories": len(by_repo), "orders": args.orders, "dimensions": DIMENSIONS, "curves": {"all": {}, "used_in_docs": {}}}
    pairs = {}
    for level in LEVELS:
        rows = [(repo, c) for repo, found in by_repo.items() for c in found if c["level"] == level]
        ids = [f"{repo}::{c['id']}" for repo, c in rows]
        saved = cache / f"{level}.npz"
        if saved.is_file() and np.load(saved, allow_pickle=False)["ids"].tolist() == ids:
            vectors = np.load(saved, allow_pickle=False)["vectors"]
        elif client is None:
            raise SystemExit(f"no saved vectors for {level} that match the scans in {saved}; give --base-url")
        else:
            vectors = embed([c["text"] for _, c in rows], client, args.model)
            np.savez(saved, ids=np.asarray(ids), vectors=vectors)
        print(f"{level}: {len(rows):,} candidates", flush=True)
        repos = [repo for repo, _ in rows]
        for subset in ("all", "used_in_docs"):
            rows_of = {repo: [] for repo in by_repo}  # every repository takes part, also with nothing at this level
            for i, (repo, c) in enumerate(rows):
                if subset == "all" or c["used_in_docs"]:
                    rows_of[repo].append(i)
            groups = [vectors[indices] if indices else np.zeros((0, DIMENSIONS), dtype=np.float32) for indices in rows_of.values()]
            result["curves"][subset][level] = {f"{t:.2f}": curve(groups, t, args.orders) for t in args.thresholds}
        pairs[level] = similar_pairs(ids, [c["text"] for _, c in rows], repos, vectors)
    (OUT / "saturation.json").write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    (OUT / "saturation.md").write_text(report(result), encoding="utf-8")
    (OUT / "saturation_pairs.md").write_text(pairs_report(pairs), encoding="utf-8")
    print("-> out/corpus/saturation.md, out/corpus/saturation_pairs.md")


if __name__ == "__main__":
    main()

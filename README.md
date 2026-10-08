# Conspiracy lore workspace

A source-linked research wiki for designing an original conspiracy-themed grand strategy game. Everything extracted here is an **attributed source claim**, not a verified description of reality.

## Start here

- [Topic wiki](wiki/index.md)
- [Continuous collection progress](reports/collection.md)
- [Progress and review notes](reports/pilot.md)
- [Source inventory](sources/manifest.json)
- [Worker instructions](AGENTS.md)

The pilot contains 20 transcript records, including two candidate English/Spanish pairs. Collection continues through successive cohorts; the current reviewed totals and remaining inventory are recorded in the progress report. Records capture compact core claims rather than every detail.

Successive cohorts are recorded under `work/cohorts/`, with immutable worker and review assignments under `work/batches/<cohort-id>/`. Four Luna extractors and two independent Luna reviewers process each cohort. Only reviewed records appear in the generated wiki. Exact snapshot duplicates can be skipped; translations and revisions require content comparison. See `scripts/continuous.py` and the progress report for resume commands.

## Data and workflow

`sources/manifest.json` records URLs, titles, metadata, and content hashes. `work/ledger.json` records processing state. Luna workers write independent `records/<source-id>.json` files. A coordinator validates evidence references, resolves topic identities, and rebuilds cross-linked Markdown pages. Game design inventions belong in `design/`, separate from source claims.

Source transcript bodies stay in a local cache outside this public repository. Published research records use short paraphrases, source URLs, and passage identifiers. The source site's commercial-use notice is recorded with each downloaded source; this project does not establish permission to adapt or republish its material commercially.

Evidence identifiers use the explicit `line-passages-v1` parsing contract: HTML block endings and line breaks separate passages. They can split speaker turns, so extraction and review must include neighboring passages when attribution or a qualification crosses a boundary. They are not the original HTML paragraph numbers or live-page anchors. This contract is retained across cohorts so citations remain stable.

## Reproduce and resume

```sh
python3 scripts/lore.py discover --index ../source-cache/index.html
python3 scripts/lore.py prepare --cache ../source-cache
python3 scripts/lore.py validate --cache ../source-cache
python3 scripts/lore.py build
python3 -m unittest discover -s tests
```

If the index cache is missing, `discover` downloads it. `prepare` caches the selected source versions and creates assignments. A changed source hash must be reviewed before old evidence references are reused. Git checkpoints preserve the inventory, extraction records, wiki, and ledger; transcript snapshots can be refetched and compared with the retained hashes.

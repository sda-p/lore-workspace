# Conspiracy lore workspace

A source-linked research wiki for designing an original conspiracy-themed grand strategy game. Everything extracted here is an **attributed source claim**, not a verified description of reality.

## Start here

- [Topic wiki](wiki/index.md)
- [Progress and review notes](reports/pilot.md)
- [Source inventory](sources/manifest.json)
- [Worker instructions](AGENTS.md)

The first batch contains 20 transcript records, including two candidate English/Spanish pairs. The full discovered inventory is retained for later batches. This pilot collects compact core claims; it is not an exhaustive extraction of every detail.

## Data and workflow

`sources/manifest.json` records URLs, titles, metadata, and content hashes. `work/ledger.json` records processing state. Luna workers write independent `records/<source-id>.json` files. A coordinator validates evidence references, resolves topic identities, and rebuilds cross-linked Markdown pages. Game design inventions belong in `design/`, separate from source claims.

Source transcript bodies stay in a local cache outside this public repository. Published research records use short paraphrases, source URLs, and passage identifiers. The source site's commercial-use notice is recorded with each downloaded source; this project does not establish permission to adapt or republish its material commercially.

Evidence identifiers use the explicit `line-passages-v1` parsing contract: HTML block endings and line breaks separate passages. They can split speaker turns, so extraction and review must include neighboring passages when attribution or a qualification crosses a boundary. They are not the original HTML paragraph numbers or live-page anchors. This contract is retained for the pilot so its citations remain stable.

## Reproduce and resume

```sh
python3 scripts/lore.py discover --index ../source-cache/index.html
python3 scripts/lore.py prepare --cache ../source-cache
python3 scripts/lore.py validate --cache ../source-cache
python3 scripts/lore.py build
python3 -m unittest discover -s tests
```

If the index cache is missing, `discover` downloads it. `prepare` caches the selected source versions and creates assignments. A changed source hash must be reviewed before old evidence references are reused. Git checkpoints preserve the inventory, extraction records, wiki, and ledger; transcript snapshots can be refetched and compared with the retained hashes.

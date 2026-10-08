# Collection pilot

## Current checkpoint

- Discovered article URLs: 2207
- Batch records validated: 20
- Reviewed underlying work groups in this batch: 18
- Source-specific claims collected: 132
- Topic pages: 19
- Batch records pending or needing correction: 0
- Catalogued URLs outside this batch: 2187

Validation checks identities, recomputed source hashes, passage references, topic references, IDs, and compact paraphrase budgets. Structural validation does not establish factual truth or semantic accuracy. This batch is a compact core extraction, with omissions retained as coverage tags.

## Review outcome

Four Luna workers extracted the initial records. A separate Luna reviewed 131 claims; the coordinator applied five evidence/scope corrections and one regional refinement. Full-language comparison identified material omitted from one English counterpart; one additional Spanish-specific claim was added and independently checked, bringing the checkpoint to 132 claims. Both translation pairs remain separate source snapshots grouped for deduplication.

The engineering review led to hash revalidation, stronger format/type checks, retained inactive ledger history, and safer Markdown output. Sixteen integrity tests pass. Line-break passage segmentation remains an explicit documented limitation.

Coverage recall was not measured against a full human extraction. Compact records do not claim to capture all available lore.

## Resume

Start from `work/ledger.json`. Recreate the source cache with `prepare`, compare retained hashes, and assign only uncompleted or explicitly expanded jobs. Candidate translations require review before one record is skipped. Do not report the entire inventory as processed.

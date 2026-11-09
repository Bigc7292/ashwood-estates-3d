# Blocked: source PDF not on box

## Expected
- Path: `/home/box/agent-data/agents/0088b415-4514-42b5-ae81-55b8ac28798b/attachments/f1abf5757fe2781876cde02bc52c3765c8c27ff621e5abfb3e2adbcced5cab93.pdf`
- Declared size: ~6.4 MB
- Filename appears to be SHA-256 of content: `f1abf5757fe2781876cde02bc52c3765c8c27ff621e5abfb3e2adbcced5cab93`

## Observed
- Agent attachments directory exists but is empty.
- Read tool and filesystem both report file not found.
- Polled repeatedly; no sync arrived.
- No workspace PDF matched that SHA-256 (searched /workspace including Barclay docs).
- Google Drive search for recent/architectural PDFs returned no files.
- User machines listed but not connected; CopyToBox unavailable.
- No external style references were supplied (recorded absent).

## Consequence
Full archivist workflow (page inspection, manifests, CAD-style rasters, ZIP package of extracts) cannot be completed without the byte-for-byte source. Substituting another local PDF would violate provenance rules.

## Retry
Place the PDF at the expected path (or pass its absolute path to `scripts/process_architectural_pdf.sh`) and re-run. Scripts and portable prompt are ready under `/workspace/plan-visuals-archive`.

# Local LLM (Ollama) setup

The corpus tooling routes mechanical LLM tasks (currently email link-ranking)
to a local Ollama model via `bin/llm.py`, falling back gracefully to Claude or
a heuristic if Ollama is unavailable. This keeps recurring Claude cost down and
keeps content on-machine.

## One-time setup
1. Install Ollama (already installed here): https://ollama.com
2. Pull the Tier-0 model: `ollama pull qwen2.5:3b`
3. Run Ollama as a background service so the daily job can reach it:
   `brew services start ollama`

## How it routes
- `bin/llm_config.py` maps capability tiers to models and holds the switches.
- `mechanical` tier → `qwen2.5:3b` (local). On failure → caller's fallback
  (rank_links → heuristic). Optional Claude Haiku middle tier: set
  `MECHANICAL_HAIKU_FALLBACK = True`.
- High-judgment work (agentic ingest, interactive ops) does NOT route here.
- Disable all local routing: set `PREFER_LOCAL = False` in `bin/llm_config.py`.

## Measuring savings
`python3 bin/llm_usage.py` prints how many calls ran local vs Claude
(reads the gitignored `raw/.llm_usage.jsonl`).

## Verifying the local path (after setup)
```bash
# router against real Ollama
python3 -c "import sys; sys.path.insert(0,'bin'); import llm; \
  r=llm.complete('Reply with ONLY JSON {\"ok\":true}', tier='mechanical', task='smoke', schema={}); \
  print(r['provider'], r['ok'], repr(r['text'])[:120])"

# rank_links end-to-end
python3 -c "import sys; sys.path.insert(0,'bin'); import rank_links as rl; \
  print(rl.rank([{'url':'https://github.com/x/y','description':'deep RAG tutorial'}, \
                 {'url':'https://news.example/funding','description':'startup raises Series A'}], \
                max_links=10, floor=4))"
```
Expect the tutorial to score high (`fetch: True`) and the funding news low
(`fetch: False, reason: low-utility`), then `python3 bin/llm_usage.py` to show
`local_ollama >= 1`.

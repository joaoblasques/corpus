---
channel: email
source: gmail
gmail_message_id: 19e6f8e8a6126447
from: "\"Shreya at AI+\" <aiplusfounderscommunity@substack.com>"
subject: "But Context First : A field guide to AI-native search"
date_received: 2026-05-28
pointer: false
collected_at: 2026-06-11
links:
  - {url: "https://substack.com/redirect/808012d7-64e2-4365-8fec-d9350319e57b?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 9, file: raw/web/zep-a-temporal-knowledge-graph-architecture-for-agent-memory.md}
  - {url: "https://substack.com/redirect/3ec98989-0854-4374-9c0b-02f3b87d9354?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 9, file: raw/web/from-local-to-global-a-graph-rag-approach-to-query-focused-s.md}
  - {url: "https://substack.com/redirect/c1cc61af-b4dd-4bed-b3ef-67032d6c6af0?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 8, file: raw/web/how-much-do-language-models-memorize.md}
  - {url: "https://substack.com/redirect/ee51c45e-2bd7-45f9-8c2f-361fa07845b2?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 8, file: raw/web/lost-in-the-middle-how-language-models-use-long-contexts.md}
  - {url: "https://substack.com/redirect/f3db7beb-8393-467a-8d09-737a913dcdf2?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 8, file: raw/web/github-getzep-graphiti-build-real-time-knowledge-graphs-for.md}
  - {url: "https://substack.com/redirect/ca35bc16-ca34-485e-9e8e-604fc3fc3d91?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 8, file: raw/web/github-567-labs-instructor-structured-outputs-for-llms.md}
  - {url: "https://substack.com/redirect/5e92f07c-bd89-46c8-84f1-ca0e504fb7b0?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 7, file: raw/web/github-mem0ai-mem0-universal-memory-layer-for-ai-agents.md}
  - {url: "https://substack.com/redirect/09e3a7b4-8c6f-4a6f-8532-0c37ae39ad86?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 7, file: raw/web/neo4j-graph-intelligence-platform.md}
corpus_ingested: true
corpus_ingested_at: 2026-06-12
corpus_pages:
  - corpus/ai-engineering/agent-memory.md
  - corpus/ai-engineering/agentic-search.md
---

View this post on the web at https://aiplusfounderscommunity.substack.com/p/but-context-first-a-field-guide-to

Every large language model on earth shares the same gorgeous, infuriating flaw: it is a genius with no memory. Brilliant and amnesiac in exactly equal measure.
Today’s models remember keywords. They do not remember relationships. They can find the three emails that mention “Priya.” They cannot tell you that Priya’s blocker got fixed, so the deal is alive again.
Thanks for reading AI+ Community! Subscribe for free to receive new posts and support my work.
That gap between retrieving text and actually remembering is the entire ballgame in 2026. AI-native search is the structural fix , not a search box with a language model bolted on the side, but a system that interprets what you actually mean and retains what actually matters, so the second conversation is sharper than the first and the tenth makes the first look quaint.
Here’s how it works under the hood. And more importantly, here’s how to check whether your AI is genuinely remembering you or just hoarding your data in a digital junk drawer.
The 3.6-bit ceiling
The instinct, when an AI forgets things, is to throw more model at it. Bigger weights, bigger context window, bigger bill. It doesn’t work, and there’s now a hard number explaining why.
In 2025, researchers from Meta’s FAIR lab, Google DeepMind, Cornell, and NVIDIA published  [ https://substack.com/redirect/c1cc61af-b4dd-4bed-b3ef-67032d6c6af0?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]How Much Do Language Models Memorize? [ https://substack.com/redirect/c1cc61af-b4dd-4bed-b3ef-67032d6c6af0?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] — and landed on a startlingly specific figure. GPT-style models can store roughly 3.6 bits of information per parameter. That’s it. To put it in human terms: 3.6 bits is about enough to pick one option out of twelve — a month of the year, or one face of a 12-sided dice. Per parameter. Models cram facts in until they hit that ceiling, and only then do they stop memorizing and start truly generalizing.
So to put it in simple terms: you can’t out-cram the problem. The memory has to live outside the model thus making it an architecture problem, not a budget one.
And the memory you bolt on the outside needs three properties that brute force genuinely cannot buy:
It must persist across sessions.
It must update when facts change.
It must stay cheap and selective at runtime.
If your “memory” disappears when the chat window closes, it was never memory, it was just a short-term recall .The memory has the be updated when things change and additionally you pay for every token, every call.Stuffing everything in "just in case" is both expensive and less accurate.
The five stages of machine memory
Think of this as the journey a single sentence takes from "raw noise hitting your system" to "your AI casually knowing the answer weeks later."
Stage 1 — Ingest:
This is basically the stage where the raw data is injested into the system, it can be anything: chat messages, call transcripts, support tickets, PDFs, CRM rows, calendar events.At this stage you do nothing clever you just capture the firehose with timestamps. The golden rule: never throw away the original. You’ll want to trace any fact back to where it came from.
The mistake almost everyone makes here: taking all this raw input, embedding it, and dumping it straight into a vector database — then calling that "memory." 
Mind the Hoarding Problem:
Say three things land in your system over a month: 
“Priya is evaluating our product,” then 
“Priya’s main blocker is SOC 2 compliance,” and later 
“SOC 2 shipped in Q2.” 
A vector store keeps all three as separate, disconnected blobs of text.
So when your rep asks “is Priya ready to buy?”, the system fetches whichever chunks sound most similar to the question, maybe it grabs the first and third, misses the second, and answers “Priya is evaluating the product” - technically true, completely useless. It never connected the blocker to the fix.
 It’s hoarding, not remembering: everything’s stored, nothing’s understood
What we want instead is a system that reads those three messages and works out what they mean as a set before it stores anything.
Stage 2 — Encoding:
Now it reads the messy text and pull out the stuff that matters. Three things, specifically:
Entity = a thing. A person, a company, a product, a city. (Priya. Lumen. Berlin.)
Attribute = a property of that thing. (Priya’s role. Lumen’s headcount. The deal’s stage.)
Edge = a relationship between two entities. (Priya works_at Lumen. Lumen headquartered_in Berlin.)
The trick that makes this reliable is a schema — a contract that says: “Don’t hand me a nice paragraph. Hand me these exact fields.” That single constraint flips the model from “regurgitate something plausible” into “actually parse this input.” Tools like Pydantic (paired with Instructor or PydanticAI) make the contract enforceable — they’ll reject anything that doesn’t fit the shape.
Here’s an extraction prompt that earns its keep. Feed it a rambling sales call and watch structure fall out the other end:
You are an entity extractor. From the transcript below, return ONLY a JSON object in this exact shape:
{
“people”:    [{ “name”, “role”, “company”, “location”, “sentiment” }],
  “companies”: [{ “name”, “industry”, “size”, “location” }],
  “intents”:   [{ “who”, “wants”, “blocker”, “timeline” }]
}
Rules:
- Use null when the text is silent. Never invent values.
- For every fact, add a “source_quote” with the exact words that justify it.
- Do not add commentary, markdown, or preamble. JSON only.
Transcript:
“Yeah so I’m Priya, I run growth over at Lumen — we’re a fintech, maybe 40 people, all remote but mostly out of Berlin. We loved the demo, the only hold-up is SOC 2. If that lands by Q3 we’re in.”
Out comes something clean and checkable:
Priya → role: Head of Growth → company: Lumen → location: Berlin; Lumen → fintech, ~40 people; intent → wants to buy, blocked on SOC 2, timeline Q3
Stage 3 — Storage:
This is the stage where storage quietly turns into memory. The temptation is to treat what you extracted as a tidy note and file it away, but a note is inert you can only ever read it back whole. Instead, you decompose it into a graph. 
Each entity Priya mentioned becomes a node: Priya herself, her company Lumen, the city Berlin. Each fact about a node becomes an attribute that hangs off it — Lumen's industry, its rough headcount. And, most importantly, each relationship becomes an edge connecting two nodes: Priya —[works_at]→ Lumen. The sentence stops being prose you re-read and becomes a path you can walk.
The edges are bi-temporal: each one carries the period for which it was true, not just the claim that it is. So when Priya later moves on, the system doesn't overwrite the past or trip over a contradiction — it marks the old edge expired, dates the new one, and keeps both. Your memory now has a sense of before and after, which is the difference between understanding a person and merely accumulating facts about them.
Stage 4 — Retrieval:
The question arrives: “Is Priya ready to buy?”
Here’s where most systems quietly cheat — they jam the entire history into the prompt and pray the answer is buried somewhere inside. This is expensive, slow, and — proven fact — unreliable.
A landmark Stanford study,  [ https://substack.com/redirect/ee51c45e-2bd7-45f9-8c2f-361fa07845b2?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]Lost in the Middle [ https://substack.com/redirect/ee51c45e-2bd7-45f9-8c2f-361fa07845b2?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ], showed that language models have a U-shaped attention curve: they reliably use information at the beginning and end of a long context, and significantly degrade when the relevant fact is stranded in the middle — even for models explicitly built for long contexts. Your perfect answer can be sitting right there in the prompt and the model will stroll right past it.
The graph lets you be a surgeon instead of a hoarder. Rather than reading everything, you locate the nodes the question touches — Priya, Lumen — and traverse outward to pull only the relevant subgraph: her role, her location, the blocker, the timeline, the fix. You do this with hybrid search, blending three signals:
Semantic meaning — so “the Lumen deal” finds the right cluster even if nobody typed those exact words.
Keyword matching — for precise terms like “SOC 2” that you don’t want fuzzed.
Graph traversal — following the actual relationships outward, hop by hop.
And because every edge is time-stamped, retrieval silently filters for what’s currently true and drops what’s expired. You feed the model a tight, relevant, current subgraph , not a 40,000-token haystack.
Stage 5 — Deliver:
The final stage is synthesis. Instead of letting the model free-associate over whatever it found, you ask for a structured answer — a response, a confidence level, and the exact sources it leaned on — grounded strictly in the subgraph you retrieved.
Weeks after that March call, your rep types: “Should we push the enterprise tier to Priya?” And the assistant answers:
“Worth it now. Priya (Head of Growth, Lumen, Berlin) was blocked on SOC 2 in your March call — that shipped in Q2, so the blocker’s gone. Deal stage is late, churn risk low. Lead with the compliance update. Confidence: high. Sources: call_0312, release_note_soc2.“
For Builders: 
If you want to build the memory layer described above rather than just understand it, here’s the open toolkit the field is converging on:
Graphiti [ https://substack.com/redirect/f3db7beb-8393-467a-8d09-737a913dcdf2?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] / Zep — the temporal knowledge graph engine behind Stage 3’s bi-temporal edges. Open source, production-grade.
Mem0 [ https://substack.com/redirect/5e92f07c-bd89-46c8-84f1-ca0e504fb7b0?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] — a popular memory layer focused on being token-efficient and selective. The 2026 benchmarks have been kind to it.
Neo4j [ https://substack.com/redirect/09e3a7b4-8c6f-4a6f-8532-0c37ae39ad86?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] — the graph database workhorse for storing nodes and edges at scale.
Pydantic + Instructor [ https://substack.com/redirect/ca35bc16-ca34-485e-9e8e-604fc3fc3d91?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] — the schema contract from Stage 2 that forces clean, structured extraction.
Steal this: audit your own AI’s memory
The Contradiction Test— does it update, or just hoard?
Prompt:
“Earlier I told you my company uses Postgres. Now I’m telling you we migrated to DynamoDB last month. If I ask what database we use, what will you say, and what happened to the old fact?”
A hoarder says “you use Postgres and DynamoDB.” A real memory says “DynamoDB now; Postgres is expired as of last month.”
The Receipts Test — can it trace a fact to a source?
Prompt:
“Tell me one thing you believe about my project, and cite exactly where you learned it. If you can’t point to a source, say so.”
If it can’t show its receipts, it’s just guessing.
The Relationship Test — does it connect facts, or just store them?
Prompt:
“Based on everything I’ve told you, what’s a conclusion you can draw that I never stated directly — by connecting two or more separate facts?”
These four papers are worth reading if you wish to understand deeper about Context Engineering:
How Much Do Language Models Memorize? [ https://substack.com/redirect/c1cc61af-b4dd-4bed-b3ef-67032d6c6af0?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] — Morris et al. (Meta FAIR, Google DeepMind, Cornell, NVIDIA, 2025). The 3.6-bits-per-parameter paper. Read this to understand why memory has to live outside the model.
Zep: A Temporal Knowledge Graph Architecture for Agent Memory [ https://substack.com/redirect/808012d7-64e2-4365-8fec-d9350319e57b?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] — Rasmussen et al. (2025). The bi-temporal graph approach, beating the previous state-of-the-art on memory benchmarks while cutting latency dramatically. This is Stage 3 made real.
Lost in the Middle: How Language Models Use Long Contexts [ https://substack.com/redirect/ee51c45e-2bd7-45f9-8c2f-361fa07845b2?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] — Liu et al. (Stanford, 2023). The U-shaped attention curve. The single best argument against “just stuff everything in the prompt.
From Local to Global: A GraphRAG Approach [ https://substack.com/redirect/3ec98989-0854-4374-9c0b-02f3b87d9354?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] — Edge et al. (Microsoft Research, 2024). How graph structure beats flat vector retrieval on big-picture questions across an entire corpus.
The takeaway isn't "vector databases are bad" or "graphs are magic." It's that memory is an architecture decision, not a feature you can buy. 
You can't out-spend a 3.6-bit ceiling. You can only build a smarter system around it, one that understands a set of facts before storing them, knows when each was true, and walks to the answer instead of drowning in the haystack.
To more learning,
Team AI+
Thanks for reading AI+ Community! Subscribe for free to receive new posts and support my work.

Unsubscribe https://substack.com/redirect/2/eyJlIjoiaHR0cHM6Ly9haXBsdXNmb3VuZGVyc2NvbW11bml0eS5zdWJzdGFjay5jb20vYWN0aW9uL2Rpc2FibGVfZW1haWw_dG9rZW49ZXlKMWMyVnlYMmxrSWpveE1EY3pPREV4TENKd2IzTjBYMmxrSWpveE9UazFPVGN4TWpnc0ltbGhkQ0k2TVRjM09UazRPREEzTWl3aVpYaHdJam94T0RFeE5USTBNRGN5TENKcGMzTWlPaUp3ZFdJdE5EYzNOemcxTVNJc0luTjFZaUk2SW1ScGMyRmliR1ZmWlcxaGFXd2lmUS4wNks2dGk3LXFZSEJCUUx3NFF3b29md0NmZ3dhYmdicVVKRTZadVFnbUlrIiwicCI6MTk5NTk3MTI4LCJzIjo0Nzc3ODUxLCJmIjp0cnVlLCJ1IjoxMDczODExLCJpYXQiOjE3Nzk5ODgwNzIsImV4cCI6MjA5NTU2NDA3MiwiaXNzIjoicHViLTAiLCJzdWIiOiJsaW5rLXJlZGlyZWN0In0.nOMXdXv1ICHulANnUAGED8xIkkNKBef8_wc99Zg1lpE?

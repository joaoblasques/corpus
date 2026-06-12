---
channel: email
source: gmail
gmail_message_id: 19eb6cdb422aac5f
from: "\"Ale from The Pipe & The Line\" <thepipeandtheline@substack.com>"
subject: AI Observability For Data Engineers (a.k.a The AI Analytics Data Pipeline)
date_received: 2026-06-11
pointer: false
collected_at: 2026-06-11
links:
  - {url: https://substack.com/redirect/923d947a-1157-4408-a9f4-9f62e0c820c6?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms, fetched: true, score: 8, file: raw/web/rest-api-client-opik-python-sdk.md}
  - {url: https://substack.com/redirect/5a8e13d3-adf3-4e37-9338-cd879f9bb7b4?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms, fetched: false, score: 8, reason: fetch-failed}
  - {url: https://substack.com/redirect/844028bf-b92b-448f-b2f0-0696de19d727?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms, fetched: true, score: 7, file: raw/web/agno-framework-for-ai-agents-opik.md}
corpus_ingested: true
corpus_ingested_at: 2026-06-11
corpus_pages:
  - corpus/data-engineering/ai-observability-data-pipeline.md
---

View this post on the web at https://thepipeandtheline.substack.com/p/ai-observability-for-data-engineers

Hi there! Alejandro here 😊
Subscribe if you like to read about technical data & AI learnings, deep dives!
Enjoy the reading and let me know in the comments what you think about it 👨🏻‍💻
📝 TL;DR
AI observability is a data pipeline. Traces are events, evaluations are quality checks. You already know how to build this
The real shift: annotators replace analysts. Instead of preparing data for dashboards, they shape agent behavior data into product decisions
The loop (observe → evaluate → act) is just CI/CD applied to agent quality instead of code quality
Data Engineering is and will be the role to set the grounds for AI to succeed. I usually hate repeating myself when writing down stuff, but this is the one thing I don’t mind repeating a lot.
On the Analytics side of things, agents need good data. We’ve heard that before.
But for anything to really perform, you need the “meta” part that comes with it.
As any other initiative in your company, AI Agents will become a new data source that you will have to pass through a data pipeline eventually, and that’s when it becomes interesting.
You can’t go through this process without understanding AI observability, the same way you can’t go through any data pipeline building process without grasping data shapes and modeling angles behind it.
When I first jumped into ETLing AI Agents sessions and traces, I started noticing many things and was grateful about the knowledge transfer I could implement here.
Everything looked familiar, and this is one of many reasons why AI & Data Engineering are not so far away once again, and it’s not only because of the data, but because Data Engineers can inspire AI Engineers (or become hybrid profiles 🤝) to catch blind spots on AI Agents the same way you would on data points.
You’ve Already Built This Pipeline
I’ll showcase all the examples in Opik, the tool for AI Observability I use at work. Most concepts are shared among other AI observability tools.
To have this tracking in place, you need to integrate using Opik’s SDK and find if your framework is supported or use an Open Telemetry integration. In my case I use Agno [ https://substack.com/redirect/844028bf-b92b-448f-b2f0-0696de19d727?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ].
Strip away the AI buzzwords and look at what’s actually happening:
Traces are events. Every agent interaction produces structured data: user input, tool calls, LLM responses, latencies, token counts. That’s an event stream, you’ve ingested these before, just from Stripe or Snowplow instead of Opik.
Evaluations are quality checks. Online evaluations scoring new traces as they arrive? That’s dbt tests running on fresh loads. “Is the response topically relevant?” is the same pattern as “Does every transaction have a valid customer_id?”
The evaluation prompt is your test logic. You version your dbt tests. Evaluation prompts need the same treatment. When I changed “Response Format Compliance” from “matches 2 of 5 formatting standards” to “matches ALL”, that’s a schema migration on my quality layer.
Saturated metrics are deprecated tests. When a metric stays at 1.0 for weeks, it’s like a dbt test that hasn’t failed in months. Either you fixed the problem (retire it) or it’s not testing anything real (replace it). You already know this instinct!
The thinking transfers completely.
Pro tip: You can look at the Opik SDK & REST API  [ https://substack.com/redirect/923d947a-1157-4408-a9f4-9f62e0c820c6?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]to understand how to update, read and do bulk processing of traces, evaluators and more to setup your data pipelines at scale.
LLM Judges vs. Code Metrics
Two tools. Different jobs. And this is the only place where I can’t map a 1:1 equivalent because data model quality checks are usually deterministic and match driven (e.g. tables have columns with empty rows or don’t, so no room for interpretation), so let’s see:
Code metrics are deterministic:
Regex patterns, JSON schema validation, URL matching, token counts. 
Fast, cheap, reproducible. 
They catch structural failures: wrong format, missing field, tool called out of sequence.
LLM judges are evaluation prompts that score agent behavior semantically. 
“Did the response address the user’s actual intent?” You can’t write a regex for that. They catch meaning failures code can’t reach.
Watch out, don’t use a model to evaluate an agent with the same model, it usually finds a way of making everything pass 😂
I will share the same eval example, to check if the agent talks in technical jargon (e.g. internal XML tags) to the user, which it shouldn’t, to understand how it looks for Code Metric and LLM Judge approaches:
Code Metric
import re
import opik
from opik.evaluation.metrics import base_metric, score_result

# Extend this list with any tags used in your system prompt
INTERNAL_TAGS = [
  "thinking", "tool_use", "tool_result", "result",
  "answer", "context", "scratchpad", "instruction",
  "system", "artifact", "function_calls",
]

class NoInternalTagLeak(base_metric.BaseMetric):
  def __init__(self, tags: list[str] = INTERNAL_TAGS):
	  super().__init__(name="no_internal_tag_leak")
	  pattern = "|".join(re.escape(t) for t in tags)
	  self._pattern = re.compile(rf"]*>", re.IGNORECASE)

  def score(self, output: str, **kwargs) -> score_result.ScoreResult:
	  matches = self._pattern.findall(output or "")
	  leaked = bool(matches)
	  return score_result.ScoreResult(
		  name=self.name,
		  value=0.0 if leaked else 1.0,
		  reason=f"Internal tags leaked to user: {set(matches)}" if leaked else None,
	  )
LLM Judge
from opik.evaluation.metrics import base_metric, score_result

class NoPromptBleed(base_metric.BaseMetric):
  def __init__(self):
	  super().__init__(name="no_prompt_bleed")

  def score(self, output: str, **kwargs) -> score_result.ScoreResult:
	  prompt = f"""You are reviewing an AI agent's response to a user.

Response:
{output}

Does the response contain any internal prompt structure that was not meant for the user? This includes XML tags (like , , ,
), JSON blobs that look like tool call payloads, raw system instructions, or any structural content that appears to be part of the agent's internal
reasoning rather than a natural reply.

Answer YES if any internal structure is visible to the user.
Answer NO if the response reads as a clean, natural reply with no internal leakage.

Reply with only YES or NO."""

	  result = self._call_llm(prompt)
	  passed = result.strip().upper() == "NO"
	  return score_result.ScoreResult(
		  name=self.name,
		  value=1.0 if passed else 0.0,
		  reason="Internal prompt structure visible in user-facing response" if not passed else None,
	  )
Same target, one more deterministic, the other relying on AI.
Thanks for reading The Pipe & The Line! This post is public so feel free to share it.
The Loop Is CI/CD for Agent Quality
Data engineers run CI/CD on pipelines. Tests on every merge. Monitoring on every load. Alerts when something drifts. Fix, redeploy, watch again.
AI observability is the same loop applied to agent behavior:
Observe (monitor): Sample production traces. Real conversations, not synthetic data. What is the agent actually doing?
Evaluate (test): Run binary checks on specific behaviors. “Did it call the right tool?” “Does the output match the source?” Same energy as “Does every row have a valid foreign key?”
Act (deploy): Turn findings into changes. Prompt refinements, tool redesigns, new capabilities. Watch the next batch of traces to see if it worked.
On repeat, find the best spot on the calendar to do this on a weekly basis depending on traffic.
Teams that struggle stop at step 1. Beautiful trace dashboards, no idea what to do with them.
If you want to go further as a Data Engineer in the era of AI, set up an LLM pipeline to review patterns on traces at scale to set up agendas on what to evaluate next, what evaluators to calibrate and what agent improvements could be executed.
What This Means for Your Metrics
Once you see observability as a pipeline, your approach to metrics changes:
Stop using generic scores. Hallucination, AnswerRelevance, ContextPrecision: the equivalent of “row count > 0” as a data quality test. Technically a test. Practically useless. You need checks specific to YOUR agent’s failure modes, just like you need tests specific to YOUR data model’s business rules.
Make every metric binary. “Did the agent call search_knowledge before citing a URL?” Yes or no. “Does the URL in the response match the tool output?” Yes or no. The litmus test: ask three people to apply it. If they all answer the same, it works.
Version your evaluation criteria. Your prompts change. Your tools change. Your agent changes. If you don’t track when and why you modified an evaluation, you can’t debug regressions. Keep a changelog.
Production data beats synthetic datasets. Use what users actually send. Weird edge cases from production surface real bugs synthetic data never would. You learned this the first time staging passed all tests and production broke anyway.
Final Words
You might notice that my recommendations go towards Data Engineers setting up evaluation criteria, not just processing the data. 
I truly believe that this part of AI projects will lie more on Data Engineers as core maintainers than AI Engineers themselves.
You need to know the logic behind anything you process, so participating in how to asses the agents are working will auto-refine what needs to be consider to build the best data grounds for them in the future.
Play with agents, develope evlauators with your quality check mindset, build automations for insights generation and keep it up to enrich your profile as much as you can for this era.
For the full implementation war story (+1000 manual reviews, annotation sessions, eval criteria refinement), read Behind the Scenes of AI Observability in Production [ https://substack.com/redirect/5a8e13d3-adf3-4e37-9338-cd879f9bb7b4?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ].
If you enjoyed the content, hit the like ❤️ button, share, comment, repost, and all those nice things people do when like stuff these days. Glad to know you made it to this part!
Hi, I am Alejandro Aboy. I am currently working as a Data Engineer. I started in digital marketing at 19. I gained experience in website tracking, advertising, and analytics. I also founded my agency. In 2021, I found my passion for data engineering. So, I shifted my career focus, despite lacking a CS degree. I’m now pursuing this path, leveraging my diverse experience and willingness to learn.

Unsubscribe https://substack.com/redirect/2/eyJlIjoiaHR0cHM6Ly90aGVwaXBlYW5kdGhlbGluZS5zdWJzdGFjay5jb20vYWN0aW9uL2Rpc2FibGVfZW1haWw_dG9rZW49ZXlKMWMyVnlYMmxrSWpveE1EY3pPREV4TENKd2IzTjBYMmxrSWpveU1EQTNPVGM0Tnpjc0ltbGhkQ0k2TVRjNE1URTRNek00Tnl3aVpYaHdJam94T0RFeU56RTVNemczTENKcGMzTWlPaUp3ZFdJdE1URTVOakl5T1NJc0luTjFZaUk2SW1ScGMyRmliR1ZmWlcxaGFXd2lmUS42eTBzcElFSElPbU8wSmhEeThuTVdjY1FDQXA3VFFGX1ppVVgtcDJfSkJzIiwicCI6MjAwNzk3ODc3LCJzIjoxMTk2MjI5LCJmIjp0cnVlLCJ1IjoxMDczODExLCJpYXQiOjE3ODExODMzODcsImV4cCI6MjA5Njc1OTM4NywiaXNzIjoicHViLTAiLCJzdWIiOiJsaW5rLXJlZGlyZWN0In0.xDnTi16hjDrt82zTw1mh_9RD8aeXe4j5Ttj2iOyv3Ws?

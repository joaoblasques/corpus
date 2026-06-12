---
channel: email
source: gmail
gmail_message_id: 19e5a2faceb517e2
from: Tech With Tim <tim@techwithtim.net>
subject: software fundamentals matter more than ever
date_received: 2026-05-24
pointer: false
collected_at: 2026-06-11
corpus_ingested: true
corpus_ingested_at: 2026-06-12
corpus_pages:
  - corpus/software-engineering/ai-assisted-development.md
---

Hey Joao,

A lot of developers hear that AI can write code and assume software fundamentals matter less now.

But I do not think that is the right way to look at it.

AI can help you move faster, but it can also help you create a bigger mess faster if you do not understand the system you are building.

That is why fundamentals matter more now, not less.

And these 5 things especially matter when you are writing code with AI.

1. Reach a shared understanding first

One failure mode with AI coding is that the AI simply does not build what you meant.

You had a clear idea in your head, but the AI produced something else. It may have followed the prompt in some technical sense, but it did not match the thing you were trying to build.

That is a requirements problem.

You and the AI have not reached the same understanding yet.

So instead of asking it to build right away, make it ask questions first. Let it push back, clarify the idea, ask about edge cases, and help you figure out what you actually want.

That matters because no one knows exactly what they want at the beginning.

2. Create a shared language

Another failure mode is that the AI starts talking around the problem because you and the AI are not using the same language.

Developers already know this from working with product teams or domain experts. The business uses one term, the code uses another, and you end up translating between both sides.

If that translation is messy, the software gets messy too.

The same thing happens with AI.

The terms in your plan, code, modules, and prompts should line up. If the project has specific domain language, AI needs to understand it too.

Because if those terms are not defined, it will guess.

And when it guesses, it can create the wrong abstraction, use the wrong naming, or connect the wrong ideas together.

3. Use feedback loops

Even when the AI builds the right thing, it may not work.

That is where feedback loops matter.

Types, tests, browser access, and automated checks give the AI a way to see when the code is wrong. Without those loops, it can generate a lot of code before realizing anything is broken.

But feedback only helps if the AI gets it fast enough.

The problem is that it often tries to do too much at once. It writes a big chunk of code, then checks it later.

That is backwards.

The rate of feedback is your speed limit.

If feedback is slow, the work needs to happen in smaller steps. That is why test-driven development fits so well with AI coding: write a test, make it pass, then refactor and improve the design.

That keeps AI from sprinting ahead and leaving you with a pile of code to untangle.

4. Make the codebase easy to test

Feedback loops only work well when the codebase is actually testable.

And testable code starts with clear boundaries.

That is why deep modules matter.

A deep module hides a meaningful amount of functionality behind a simple interface. You can test behavior at the boundary without understanding every tiny internal detail.

A shallow module does the opposite. It spreads complexity across too many small pieces, which makes the code harder for both you and the AI to understand later.

AI can create shallow, scattered code very easily.

It may look modular because there are lots of small files, but in practice, it becomes harder to review, harder to test, and harder to change.

5. Design the interface, then delegate the implementation

AI works best when you give it the right boundary.

You cannot review every tiny implementation detail forever, especially in lower-risk parts of the system.

That is the useful split.

You design the interface, understand the module, and define what the code should do from the outside. Then AI can help implement what happens inside.

For some parts of an application, you do not need to inspect every internal detail if the outside boundary is clear, the purpose is clear, and the behavior is testable.

But this only works if you are still thinking about the system. You still need to know which modules are changing, which interfaces matter, and which parts are too critical to delegate casually.

AI can help with implementation, but the system design still belongs to you.

AI can make you faster, but fundamentals keep that speed from turning into chaos.

The developers who get the most out of AI will not be the ones who ignore the code and hope the tool figures everything out.

They will be the ones who understand enough to guide it.

AI did not make software fundamentals optional.

It made them more important.

Talk soon,

Tim

​Unsubscribe ( https://7ec49fe4.unsubscribe.kit-mail3.com/wvuez22ngqbghkpd77zt7hnd729gki8hlelwn ) | Update your profile ( https://preferences.kit-mail3.com/wvuez22ngqbghkpd77zt7hnd729gki8hlelwn ) | 600 1st Ave, Ste 330 PMB 92768, Seattle, WA 98104-2246

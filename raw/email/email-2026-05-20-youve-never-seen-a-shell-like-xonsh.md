---
channel: email
source: gmail
gmail_message_id: 19e458a9d79d8db5
from: DevOps Toolbox <omer@dotb.sh>
subject: You’ve Never Seen a Shell Like Xonsh
date_received: 2026-05-20
pointer: false
collected_at: 2026-06-11
links:
  - {url: "https://24c788c2.click.kit-mail3.com/e5u72xk360h7hlg8nwou8h85xpkowalhgdox8/owhkhqhwvn2versv/aHR0cHM6Ly9sZWFybi5vbWVyeHguY29tL2NvdXJzZXMvazhzLWZyb20tc2NyYXRjaA==", fetched: false, score: 7, reason: fetch-failed}
  - {url: "https://24c788c2.click.kit-mail3.com/e5u72xk360h7hlg8nwou8h85xpkowalhgdox8/z2hghnhev7qvzeip/aHR0cHM6Ly9jbGljay5jb252ZXJ0a2l0LW1haWwyLmNvbS9vOHV4bHo3d3F4YXFoazAzMzRvdXZocXJnbzdycnVvL293aGtocWhydjRwcWRxYnYvYUhSMGNITTZMeTlzWldGeWJpNXZiV1Z5ZUhndVkyOXRMMk52ZFhKelpYTXZjMlZqYjI1a0xXSnlZV2x1TFc1bGIzWnBiUT09", fetched: false, score: 6, reason: fetch-failed}
  - {url: "https://24c788c2.click.kit-mail3.com/e5u72xk360h7hlg8nwou8h85xpkowalhgdox8/e0hph7h7ge8gzni8/aHR0cHM6Ly9mYW5kZi5jby80d0h1bUxx", fetched: false, score: 1, reason: low-utility}
  - {url: "https://fandf.co/4wHumLq", fetched: false, score: 1, reason: low-utility}
  - {url: "https://24c788c2.click.kit-mail3.com/e5u72xk360h7hlg8nwou8h85xpkowalhgdox8/p8heh9h40dn0eguq/aHR0cHM6Ly9idWlsdHdpdGgua2l0LW1haWwzLmNvbT91dG1fY2FtcGFpZ249cG93ZXJlZGJ5JnV0bV9jb250ZW50PWVtYWlsJnV0bV9tZWRpdW09cmVmZXJyYWwmdXRtX3NvdXJjZT1keW5hbWlj", fetched: false, score: 1, reason: low-utility}
  - {url: "https://24c788c2.click.kit-mail3.com/e5u72xk360h7hlg8nwou8h85xpkowalhgdox8/7qh7h8h978r7e0az/aHR0cHM6Ly9jbGljay5jb252ZXJ0a2l0LW1haWwyLmNvbS9vOHV4bHo3d3F4YXFoazAzMzRvdXZocXJnbzdycnVvL2UwaHBoN2gwZ2s2cm8zaDgvYUhSMGNITTZMeTkwZDJsMGRHVnlMbU52YlM5a1pYWnZjSE4wYjI5c1ltOTQ=", fetched: false, score: 0, reason: low-utility}
corpus_ingested: true
corpus_ingested_at: 2026-06-12
corpus_pages:
  - corpus/software-engineering/developer-tooling.md
---

​

************************************
You’ve Never Seen a Shell Like Xonsh
************************************

​

This issue is brought to you by:
​

Redis Iris:
Your agents should be getting smarter
-------------------------------------

​
Unreliable agents fail in production. Redis Iris is a unified, real-time context engine that delivers fresh, relevant context so agents perform at scale.

​

-->Try for FREE ( https://24c788c2.click.kit-mail3.com/e5u72xk360h7hlg8nwou8h85xpkowalhgdox8/e0hph7h7ge8gzni8/aHR0cHM6Ly9mYW5kZi5jby80d0h1bUxx )
Try for FREE ( https://fandf.co/4wHumLq )

​
Tell me if this sounds familiar:
You start with a quick shell script.
Then one step gets annoying, so you call Python.
Then Python needs to shell out again.
Then you’re parsing strings, juggling quoting, and hoping the whole thing still works next week.
It’s not that bash is bad at being a shell.
It’s that we keep asking it to become a programming language, and that’s where the duct tape starts showing.

Xonsh doesn’t make you choose between shell commands and Python.
It basically says: keep your pipes, keep your terminal habits, but stop pretending bash is a great programming language once the script gets real.

What I learned is that Xonsh is not just “Python inside a shell.”
It’s a shell built around a Python superset, which is a very different thing.
You still get things like cd, pipes, aliases, env vars, and normal command execution, but now you also get imports, objects, functions, autocompletion, syntax highlighting (!!), and the standard library right there in the same place.
That’s a big deal if your shell scripts usually end up turning into a weird bash-to-python-to-subprocess mess.

The way I’d put this into action is pretty simple: don’t treat Xonsh as a universal bash replacement.
Treat it like the shell you reach for when your workflow is getting too "smart" for plain shell scripting but still too shell heavy for pure Python.
That means local automation, little helper scripts, data wrangling, tool glue, AI driven workflows, and anything where you keep jumping between CLI commands and Python logic.
Does this mean I'd slap it on every production machine?
No.
But would I set it as a sidekick shell locally?
100% yes.

The usual fix is a split-brain workflow
---------------------------------------

Most of us solve this the same way: use bash for command execution, then switch to Python once the logic gets serious.
That works, kind of.
Bash stays the glue.
Python does the heavy lifting.
If something shell like is needed again, python calls a subprocess and we keep moving.
It’s a very normal setup, and honestly, most of us have lived in that pattern for years.

​
It works, but it keeps fighting you
-----------------------------------

The problem is the handoff.
Python is structured and typed (yea yea don't get stingy about the types, you get the point).
So every time you jump between them, you pay for it.
You deal with quoting. You deal with env var weirdness.
You deal with subprocess calls for things that should have been simple.
Even when it works, it rarely feels clean.
​

Same shell habits, better building blocks
-----------------------------------------

What makes Xonsh interesting is that it keeps the shell feel while giving you python as a first class tool. You can do quick shell stuff, then immediately import a library, inspect objects, write a function, or manipulate structured data without leaving the session (yes, keep your nushell comments 😉).
Env vars can be read directly like strings.

~ ➜ print($EDITOR)
nvim

​
Python objects are right there.
You can append to your PATH without doing Bash surgery:

~ ❯ $PATH.append('/opt/mytools/bin')
You can capture command output and inspect metadata like stdout, stderr, return code, and process details.
Aliases live as objects.
Functions can mix shell commands and Python logic.
That’s the part that feels genuinely different.

​

Not magic.. just a better tradeoff
----------------------------------

There are still limits - Xonsh is not POSIX compatible enough to blindly use everywhere.
But people use this statement to cancel too many great options.
There's a spectrum there - Nushell is not posix compatible but it's at an extreme where to set an env var you have to -

$.env.PATH = ...
# and don't forget to wrap '=' with spaces :(

It doesn't have to be that extreme, and Xonsh - is more forgiving in that regard.
I wouldn’t make it my login shell on production boxes just because it looks cool.
Also, if you love Nushell for structured tables and built-in data handling, Xonsh won’t beat it at every data shaped task.
You’ll probably still reach for jq sometimes, and that’s fine.
But if your main pain is that bash gets ugly the second your script grows up, Xonsh feels like a much better tradeoff.
​

My takeaway
-----------

If you write a lot of automation, shell helpers, homelab scripts, CI glue, or event agent workflows, Xonsh is worth testing for a couple of weeks.
About these "agents workflows" imagine just having your AI compose scripts to automate your shell in a language that's READABLE.
And yea, I've written thousands of bash lines, it's great for short stuff, but if you automated something slightly complicated, and let an agent write it for you, you're NOT going to enjoy the review process, don't ask me how I know.
(if you're in the "I don't review anymore" crowd - move on).
​
Xonsh won’t be the right shell for everyone, but I totally get why it’s getting attention again.
The world changed.
More of our terminal work now wants a real language behind it.
​

I hope this was valuable! Thank you for reading.

Feel free to reply directly with any question or feedback.

Have a great weekend!

Whenever you’re ready, here’s how I can help you:

​

* ​Follow me on X / Twitter ( https://24c788c2.click.kit-mail3.com/e5u72xk360h7hlg8nwou8h85xpkowalhgdox8/7qh7h8h978r7e0az/aHR0cHM6Ly9jbGljay5jb252ZXJ0a2l0LW1haWwyLmNvbS9vOHV4bHo3d3F4YXFoazAzMzRvdXZocXJnbzdycnVvL2UwaHBoN2gwZ2s2cm8zaDgvYUhSMGNITTZMeTkwZDJsMGRHVnlMbU52YlM5a1pYWnZjSE4wYjI5c1ltOTQ= )
* ​Zero To KNOWING Kubernetes in Under 90 Minutes ( https://24c788c2.click.kit-mail3.com/e5u72xk360h7hlg8nwou8h85xpkowalhgdox8/owhkhqhwvn2versv/aHR0cHM6Ly9sZWFybi5vbWVyeHguY29tL2NvdXJzZXMvazhzLWZyb20tc2NyYXRjaA== )​
* ​Building a Second Brain with Neovim in Under 90 Minutes ( https://24c788c2.click.kit-mail3.com/e5u72xk360h7hlg8nwou8h85xpkowalhgdox8/z2hghnhev7qvzeip/aHR0cHM6Ly9jbGljay5jb252ZXJ0a2l0LW1haWwyLmNvbS9vOHV4bHo3d3F4YXFoazAzMzRvdXZocXJnbzdycnVvL293aGtocWhydjRwcWRxYnYvYUhSMGNITTZMeTlzWldGeWJpNXZiV1Z5ZUhndVkyOXRMMk52ZFhKelpYTXZjMlZqYjI1a0xXSnlZV2x1TFc1bGIzWnBiUT09 )​

​

Unsubscribe ( https://24c788c2.unsubscribe.kit-mail3.com/e5u72xk360h7hlg8nwou8h85xpkowalhgdox8 ) | Update your profile ( https://preferences.kit-mail3.com/e5u72xk360h7hlg8nwou8h85xpkowalhgdox8 ) | 600 1st Ave, Ste 330 PMB 92768, Seattle, WA 98104-2246

( https://24c788c2.click.kit-mail3.com/e5u72xk360h7hlg8nwou8h85xpkowalhgdox8/p8heh9h40dn0eguq/aHR0cHM6Ly9idWlsdHdpdGgua2l0LW1haWwzLmNvbT91dG1fY2FtcGFpZ249cG93ZXJlZGJ5JnV0bV9jb250ZW50PWVtYWlsJnV0bV9tZWRpdW09cmVmZXJyYWwmdXRtX3NvdXJjZT1keW5hbWlj )

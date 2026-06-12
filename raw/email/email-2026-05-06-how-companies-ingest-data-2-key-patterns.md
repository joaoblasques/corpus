---
channel: email
source: gmail
gmail_message_id: 19dfd60ac03ede3d
from: StartDataEngineering <joseph.machado@startdataengineering.com>
subject: "How Companies Ingest Data: 2 Key Patterns"
date_received: 2026-05-06
pointer: false
collected_at: 2026-06-11
links:
  - {url: "https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/08hwh9h2r5qr8qal/aHR0cHM6Ly93d3cuc3RhcnRkYXRhZW5naW5lZXJpbmcuY29tL3Bvc3QvZGF0YS1sb2FkaW5nLXBhdHRlcm5zLw==", fetched: true, score: 7, file: raw/web/how-to-ingest-data-2-essential-patterns-start-data-engineeri.md}
  - {url: "https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/vqh3hrhor78r5lig/aHR0cHM6Ly93d3cuc3RhcnRkYXRhZW5naW5lZXJpbmcuY29tLw==", fetched: true, score: 6, file: raw/web/master-data-engineering-always-be-in-demand.md}
  - {url: "https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/8ghqhohonvkn4wuk/aHR0cHM6Ly9wb2xscy5raXQuY29tLzQyMzk0P29wdGlvbl9pZD0xNTI4MzUmdG9rZW49d3Z1ZTM5MnZsOXVnaGtwbzhteHU3aG5kZHp2ZW90OGhxcXA5Mg==", fetched: false, score: 1, reason: low-utility}
  - {url: "https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/8ghqhohonvkn4wuk/aHR0cHM6Ly9wb2xscy5raXQuY29tLzQyMzk0P29wdGlvbl9pZD0xNTI4MzYmdG9rZW49d3Z1ZTM5MnZsOXVnaGtwbzhteHU3aG5kZHp2ZW90OGhxcXA5Mg==", fetched: false, score: 1, reason: low-utility}
  - {url: "https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/8ghqhohonvkn4wuk/aHR0cHM6Ly9wb2xscy5raXQuY29tLzQyMzk0P29wdGlvbl9pZD0xNTI4MzcmdG9rZW49d3Z1ZTM5MnZsOXVnaGtwbzhteHU3aG5kZHp2ZW90OGhxcXA5Mg==", fetched: false, score: 1, reason: low-utility}
  - {url: "https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/8ghqhohonvkn4wuk/aHR0cHM6Ly9wb2xscy5raXQuY29tLzQyMzk0P29wdGlvbl9pZD0xNTI4MzgmdG9rZW49d3Z1ZTM5MnZsOXVnaGtwbzhteHU3aG5kZHp2ZW90OGhxcXA5Mg==", fetched: false, score: 1, reason: low-utility}
  - {url: "https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/8ghqhohonvkn4wuk/aHR0cHM6Ly9wb2xscy5raXQuY29tLzQyMzk0P29wdGlvbl9pZD0xNTI4MzkmdG9rZW49d3Z1ZTM5MnZsOXVnaGtwbzhteHU3aG5kZHp2ZW90OGhxcXA5Mg==", fetched: false, score: 1, reason: low-utility}
  - {url: "https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/8ghqhohonvkn4wuk/aHR0cHM6Ly9wb2xscy5raXQuY29tLzQyMzk0P29wdGlvbl9pZD0xNTI4NDAmdG9rZW49d3Z1ZTM5MnZsOXVnaGtwbzhteHU3aG5kZHp2ZW90OGhxcXA5Mg==", fetched: false, score: 1, reason: low-utility}
  - {url: "https://preferences.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92", fetched: false, score: 0, reason: low-utility}
  - {url: "https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/l2hehmhl79w7g2f6/aHR0cHM6Ly9idWlsdHdpdGgua2l0LW1haWwzLmNvbT91dG1fY2FtcGFpZ249cG93ZXJlZGJ5JnV0bV9jb250ZW50PWVtYWlsJnV0bV9tZWRpdW09cmVmZXJyYWwmdXRtX3NvdXJjZT1keW5hbWlj", fetched: false, score: 0, reason: low-utility}
corpus_ingested: true
corpus_ingested_at: 2026-06-12
corpus_pages:
  - corpus/data-engineering/data-ingestion-patterns.md
---

Hello Joao Blasques,

Most companies ingest data in one of two ways.

* Stream data into a cloud store via an event log like Kafka.
* Extract data from source systems in batch.

In this article 👇, we go over a high-level design of how they are
built and their tradeoffs.

​> Data Ingestion Patterns (
https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/08hwh9h2r5qr8qal/aHR0cHM6Ly93d3cuc3RhcnRkYXRhZW5naW5lZXJpbmcuY29tL3Bvc3QvZGF0YS1sb2FkaW5nLXBhdHRlcm5zLw==
)​

I am continually improving my content to better serve you.
Recently, I launched a Data Engineering Course.

Could you please let me know why you did not enroll?

This data helps me better serve my readers. I really appreciate
any feedback.

What was the main reason you didn't enroll in "The Data
Engineering Course"?

-->
(
https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/8ghqhohonvkn4wuk/aHR0cHM6Ly9wb2xscy5raXQuY29tLzQyMzk0P29wdGlvbl9pZD0xNTI4MzUmdG9rZW49d3Z1ZTM5MnZsOXVnaGtwbzhteHU3aG5kZHp2ZW90OGhxcXA5Mg==
)
The price was too high (
https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/8ghqhohonvkn4wuk/aHR0cHM6Ly9wb2xscy5raXQuY29tLzQyMzk0P29wdGlvbl9pZD0xNTI4MzUmdG9rZW49d3Z1ZTM5MnZsOXVnaGtwbzhteHU3aG5kZHp2ZW90OGhxcXA5Mg==
)

-->
(
https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/8ghqhohonvkn4wuk/aHR0cHM6Ly9wb2xscy5raXQuY29tLzQyMzk0P29wdGlvbl9pZD0xNTI4MzYmdG9rZW49d3Z1ZTM5MnZsOXVnaGtwbzhteHU3aG5kZHp2ZW90OGhxcXA5Mg==
)
I need to learn SQL and Python first (
https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/8ghqhohonvkn4wuk/aHR0cHM6Ly9wb2xscy5raXQuY29tLzQyMzk0P29wdGlvbl9pZD0xNTI4MzYmdG9rZW49d3Z1ZTM5MnZsOXVnaGtwbzhteHU3aG5kZHp2ZW90OGhxcXA5Mg==
)

-->
(
https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/8ghqhohonvkn4wuk/aHR0cHM6Ly9wb2xscy5raXQuY29tLzQyMzk0P29wdGlvbl9pZD0xNTI4MzcmdG9rZW49d3Z1ZTM5MnZsOXVnaGtwbzhteHU3aG5kZHp2ZW90OGhxcXA5Mg==
)
The timing wasn't right (
https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/8ghqhohonvkn4wuk/aHR0cHM6Ly9wb2xscy5raXQuY29tLzQyMzk0P29wdGlvbl9pZD0xNTI4MzcmdG9rZW49d3Z1ZTM5MnZsOXVnaGtwbzhteHU3aG5kZHp2ZW90OGhxcXA5Mg==
)

-->
(
https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/8ghqhohonvkn4wuk/aHR0cHM6Ly9wb2xscy5raXQuY29tLzQyMzk0P29wdGlvbl9pZD0xNTI4MzgmdG9rZW49d3Z1ZTM5MnZsOXVnaGtwbzhteHU3aG5kZHp2ZW90OGhxcXA5Mg==
)
I have free alternatives (
https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/8ghqhohonvkn4wuk/aHR0cHM6Ly9wb2xscy5raXQuY29tLzQyMzk0P29wdGlvbl9pZD0xNTI4MzgmdG9rZW49d3Z1ZTM5MnZsOXVnaGtwbzhteHU3aG5kZHp2ZW90OGhxcXA5Mg==
)

-->
(
https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/8ghqhohonvkn4wuk/aHR0cHM6Ly9wb2xscy5raXQuY29tLzQyMzk0P29wdGlvbl9pZD0xNTI4MzkmdG9rZW49d3Z1ZTM5MnZsOXVnaGtwbzhteHU3aG5kZHp2ZW90OGhxcXA5Mg==
)
I wasn't sure it was for me (
https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/8ghqhohonvkn4wuk/aHR0cHM6Ly9wb2xscy5raXQuY29tLzQyMzk0P29wdGlvbl9pZD0xNTI4MzkmdG9rZW49d3Z1ZTM5MnZsOXVnaGtwbzhteHU3aG5kZHp2ZW90OGhxcXA5Mg==
)

-->
(
https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/8ghqhohonvkn4wuk/aHR0cHM6Ly9wb2xscy5raXQuY29tLzQyMzk0P29wdGlvbl9pZD0xNTI4NDAmdG9rZW49d3Z1ZTM5MnZsOXVnaGtwbzhteHU3aG5kZHp2ZW90OGhxcXA5Mg==
)
Something else (
https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/8ghqhohonvkn4wuk/aHR0cHM6Ly9wb2xscy5raXQuY29tLzQyMzk0P29wdGlvbl9pZD0xNTI4NDAmdG9rZW49d3Z1ZTM5MnZsOXVnaGtwbzhteHU3aG5kZHp2ZW90OGhxcXA5Mg==
)

​

Please reply to this email if you have any
questions/thoughts/ideas and I will get back to you.

Regards,

Joseph Machado

​startdataengineering.com (
https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/vqh3hrhor78r5lig/aHR0cHM6Ly93d3cuc3RhcnRkYXRhZW5naW5lZXJpbmcuY29tLw==
)​

Thanks for reading! If you loved it, tell your friends to
subscribe.

If you didn’t enjoy the email you can unsubscribe here (
https://aeca76e5.unsubscribe.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92
).

To change your email or preferences manage your profile (
https://preferences.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92
).

113 Cherry St #92768,, Seattle, WA 98104-2205

(
https://aeca76e5.click.kit-mail3.com/wvue392vl9ughkpo8mxu7hnddzveot8hqqp92/l2hehmhl79w7g2f6/aHR0cHM6Ly9idWlsdHdpdGgua2l0LW1haWwzLmNvbT91dG1fY2FtcGFpZ249cG93ZXJlZGJ5JnV0bV9jb250ZW50PWVtYWlsJnV0bV9tZWRpdW09cmVmZXJyYWwmdXRtX3NvdXJjZT1keW5hbWlj
)

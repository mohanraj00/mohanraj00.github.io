---
layout: page
title: Tech
permalink: /tech/
---

Engineering writeups: architecture, technology deep-dives, operating models, and how tech teams are built and run. No cadence; published when it has consequences.

{% for post in site.tech reversed %}
- [{{ post.title }}]({{ post.url }}) · {{ post.date | date: "%b %d, %Y" }}
{% endfor %}

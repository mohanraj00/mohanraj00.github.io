---
layout: home
title: Home
---

I build alone. AI coding agents carry the whole gamut of my work, and I keep two writing threads here:

**[Tech](/tech/)** — engineering writeups for senior techies: architecture, technology deep-dives, operating models, tech team organization. Published only when the content has consequences.

**[Midweek Synapse](/synapse/)** — syntheses from my second-brain wiki: archaeology, astronomy, economics, Indian philosophy, and whatever else sticks.

## Latest — Tech

{% for post in site.tech reversed limit: 5 %}
- [{{ post.title }}]({{ post.url }}) — {{ post.date | date: "%b %d, %Y" }}
{% endfor %}

## Latest — Midweek Synapse

{% for post in site.synapse reversed limit: 5 %}
- [{{ post.title }}]({{ post.url }}) — {{ post.date | date: "%b %d, %Y" }}
{% endfor %}

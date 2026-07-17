---
layout: page
title: Midweek Synapse
permalink: /synapse/
---

Syntheses from my second-brain wiki, published midweek when a thread connects.

{% for post in site.synapse reversed %}
- [{{ post.title }}]({{ post.url }}) · {{ post.date | date: "%b %d, %Y" }}
{% endfor %}

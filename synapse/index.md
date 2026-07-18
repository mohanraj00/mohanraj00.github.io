---
layout: synapse-home
title: Midweek Synapse
permalink: /synapse/
---

Every Wednesday I pull a thread from my second brain and chase a new idea, usually where two fields
meet. It is my quest to understand a bit more, and wire up a new synapse. Learn along with me.

The 60-second versions live at [@vinavu_ai](https://instagram.com/vinavu_ai).

<ul class="synapse-list">
{% for post in site.synapse reversed %}
  <li class="synapse-item">
    <a class="synapse-item-title" href="{{ post.url | relative_url }}">{{ post.title }}</a>
    <p class="synapse-item-meta">
      {% if post.synapse %}#{{ post.synapse }} · {% endif %}{{ post.date | date: "%b %-d, %Y" }}
    </p>
    {% if post.excerpt %}<p class="synapse-item-excerpt">{{ post.excerpt | strip_html | strip }}</p>{% endif %}
  </li>
{% endfor %}
</ul>

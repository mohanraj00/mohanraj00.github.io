---
layout: page
title: Midweek Synapse
permalink: /synapse/
---

Every Wednesday I pull a thread from my second brain and chase a new idea, usually where two fields
meet. It is my quest to understand a bit more, and wire up a new synapse. Learn along with me.

The 60-second versions live at [@vinavu.ai](https://instagram.com/vinavu.ai).

<link rel="stylesheet" href="{{ '/assets/css/synapse.css' | relative_url }}">

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

<style>
.synapse-list { list-style: none; margin: 2rem 0 0; padding: 0; }
.synapse-item { padding: 1.2rem 0; border-top: 1px solid #e3e7ec; }
.synapse-item-title { font-size: 1.18rem; font-weight: 700; text-decoration: none; }
.synapse-item-meta { margin: 0.25rem 0 0.5rem; font-size: 0.8rem; color: #8a93a2;
  text-transform: uppercase; letter-spacing: 0.04em; }
.synapse-item-excerpt { margin: 0; color: #5b6472; line-height: 1.6; }
@media (prefers-color-scheme: dark) {
  .synapse-item { border-top-color: rgba(255,255,255,0.12); }
  .synapse-item-excerpt { color: #9aa6b6; }
}
</style>

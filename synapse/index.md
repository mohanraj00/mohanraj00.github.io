---
layout: synapse-home
title: Midweek Synapse
permalink: /synapse/
image: /assets/heroes/synapse.png
description: "Every Wednesday I pull a thread from my second brain and chase a new idea, usually where two fields meet."
---

Every Wednesday I pull a thread from my second brain and chase a new idea, usually where two fields
meet. It is my quest to understand a bit more, and wire up a new synapse. Learn along with me.

The 60-second versions live at [@vinavu_ai](https://instagram.com/vinavu_ai).

<ul class="post-list">
{% for post in site.synapse reversed %}
  <li class="post-item">
    <a href="{{ post.url | relative_url }}" aria-hidden="true" tabindex="-1">
      <img class="post-item-thumb" src="{{ post.image | relative_url }}" alt="" loading="lazy" width="1600" height="840">
    </a>
    <div>
      <a class="post-item-title" href="{{ post.url | relative_url }}">{{ post.title }}</a>
      <p class="post-item-meta">
        {% if post.synapse %}#{{ post.synapse }} · {% endif %}{{ post.date | date: "%b %-d, %Y" }}
      </p>
      {% if post.excerpt %}<p class="post-item-excerpt">{{ post.excerpt | strip_html | strip | truncate: 220 }}</p>{% endif %}
    </div>
  </li>
{% endfor %}
</ul>

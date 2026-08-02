---
layout: page
title: Tech
permalink: /tech/
image: /assets/heroes/tech.png
description: "Engineering writeups: architecture, technology deep-dives, operating models, and how tech teams are built and run."
---

Engineering writeups: architecture, technology deep-dives, operating models, and how tech teams are built and run. No cadence; published when it has consequences.

<ul class="post-list">
{% for post in site.tech reversed %}
  <li class="post-item">
    <a href="{{ post.url | relative_url }}" aria-hidden="true" tabindex="-1">
      <img class="post-item-thumb" src="{{ post.image | relative_url }}" alt="" loading="lazy" width="1600" height="840">
    </a>
    <div>
      <a class="post-item-title" href="{{ post.url | relative_url }}">{{ post.title }}</a>
      <p class="post-item-meta">{{ post.date | date: "%b %-d, %Y" }}</p>
      {% if post.excerpt %}<p class="post-item-excerpt">{{ post.excerpt | strip_html | strip | truncate: 220 }}</p>{% endif %}
    </div>
  </li>
{% endfor %}
</ul>

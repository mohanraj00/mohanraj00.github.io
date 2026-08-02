---
layout: home
image: /assets/heroes/home.png
---

I build alone. AI coding agents carry the whole gamut of my work, and I keep two writing threads here:

**[Tech](/tech/)**: engineering writeups for senior techies. Architecture, technology deep-dives, operating models, tech team organization. Published only when the content has consequences.

**[Midweek Synapse](/synapse/)**: syntheses from my second-brain wiki. Archaeology, astronomy, economics, Indian philosophy, and whatever else sticks.

## Latest in Tech

<!-- `reversed limit: 3` would take the first three and THEN reverse them, i.e.
     list the three oldest. Reverse into a variable first. -->
{% assign latest_tech = site.tech | reverse %}
<ul class="post-list">
{% for post in latest_tech limit: 3 %}
  <li class="post-item">
    <a href="{{ post.url | relative_url }}" aria-hidden="true" tabindex="-1">
      <img class="post-item-thumb" src="{{ post.image | relative_url }}" alt="" loading="lazy" width="1600" height="840">
    </a>
    <div>
      <a class="post-item-title" href="{{ post.url | relative_url }}">{{ post.title }}</a>
      <p class="post-item-meta">{{ post.date | date: "%b %-d, %Y" }}</p>
      {% if post.excerpt %}<p class="post-item-excerpt">{{ post.excerpt | strip_html | strip | truncate: 180 }}</p>{% endif %}
    </div>
  </li>
{% endfor %}
</ul>

## Latest in Midweek Synapse

{% if site.synapse.size > 0 %}
{% assign latest_synapse = site.synapse | reverse %}
<ul class="post-list">
{% for post in latest_synapse limit: 3 %}
  <li class="post-item">
    <a href="{{ post.url | relative_url }}" aria-hidden="true" tabindex="-1">
      <img class="post-item-thumb" src="{{ post.image | relative_url }}" alt="" loading="lazy" width="1600" height="840">
    </a>
    <div>
      <a class="post-item-title" href="{{ post.url | relative_url }}">{{ post.title }}</a>
      <p class="post-item-meta">
        {% if post.synapse %}#{{ post.synapse }} · {% endif %}{{ post.date | date: "%b %-d, %Y" }}
      </p>
      {% if post.excerpt %}<p class="post-item-excerpt">{{ post.excerpt | strip_html | strip | truncate: 180 }}</p>{% endif %}
    </div>
  </li>
{% endfor %}
</ul>
<p><a href="{{ '/synapse/' | relative_url }}">All installments →</a></p>
{% else %}
First installment lands here soon; the series currently runs on LinkedIn.
{% endif %}

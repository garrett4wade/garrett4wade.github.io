---
layout: page
permalink: /cv/
title: CV
nav: true
nav_order: 5
toc:
  sidebar: left
---

<div class="cv">
  <!-- Contact Information -->
  <div class="card mt-3 p-3">
    <h3 class="card-title font-weight-medium">Contact Information</h3>
    <div class="row">
      <div class="col-sm-6">
        <strong>Name:</strong> {{ site.data.cv.name }}<br>
        <strong>Email:</strong> {{ site.data.cv.email }}<br>
      </div>
      <div class="col-sm-6">
        <strong>Location:</strong> {{ site.data.cv.location }}<br>
        <strong>GitHub:</strong> {{ site.data.cv.github }}<br>
      </div>
    </div>
  </div>

  <!-- Education -->
  <div class="card mt-3 p-3">
    <h3 class="card-title font-weight-medium">Education</h3>
    <div>
      {% for edu in site.data.cv.education %}
        <div class="row mb-3">
          <div class="col-sm-9">
            <strong>{{ edu.degree }}</strong><br>
            <em>{{ edu.institution }}</em>, {{ edu.location }}
            {% if edu.advisor %}
              <br><strong>Advisor:</strong> {{ edu.advisor }}
            {% endif %}
            {% if edu.research_direction %}
              <br><strong>Research Direction:</strong> {{ edu.research_direction }}
            {% endif %}
            {% if edu.thesis %}
              <br><strong>Thesis:</strong> {{ edu.thesis }}
            {% endif %}
          </div>
          <div class="col-sm-3 text-right">
            <span class="badge badge-light">{{ edu.dates }}</span>
          </div>
        </div>
        {% unless forloop.last %}<hr>{% endunless %}
      {% endfor %}
    </div>
  </div>

  <!-- Publications -->
  <div class="card mt-3 p-3">
    <h3 class="card-title font-weight-medium">Publications</h3>
    <div>
      {% assign pubs_by_year = site.data.cv.publications | group_by: 'year' | sort: 'name' | reverse %}
      {% for year_group in pubs_by_year %}
        <h5 class="mt-4 mb-3">{{ year_group.name }}</h5>
        {% for pub in year_group.items %}
          <div class="mb-3">
            <strong>{{ pub.title }}</strong><br>
            <small class="text-muted">{{ pub.authors }}</small><br>
            <em>{{ pub.venue }}</em>
            {% if pub.note %}
              <span class="badge badge-info ml-2">{{ pub.note }}</span>
            {% endif %}
          </div>
        {% endfor %}
      {% endfor %}
    </div>
  </div>

  <!-- Experience -->
  <div class="card mt-3 p-3">
    <h3 class="card-title font-weight-medium">Experience</h3>
    <div>
      {% for exp in site.data.cv.experience %}
        <div class="row mb-3">
          <div class="col-sm-9">
            <strong>{{ exp.position }}</strong><br>
            <em>{{ exp.company }}</em><br>
            <small class="text-muted">{{ exp.description }}</small>
          </div>
          <div class="col-sm-3 text-right">
            <span class="badge badge-light">{{ exp.dates }}</span>
          </div>
        </div>
        {% unless forloop.last %}<hr>{% endunless %}
      {% endfor %}
    </div>
  </div>

  <!-- Awards -->
  <div class="card mt-3 p-3">
    <h3 class="card-title font-weight-medium">Awards</h3>
    <div>
      {% for award in site.data.cv.awards %}
        <div class="row mb-2">
          <div class="col-sm-9">
            <strong>{{ award.name }}</strong>
          </div>
          <div class="col-sm-3 text-right">
            <span class="badge badge-light">{{ award.year }}</span>
          </div>
        </div>
      {% endfor %}
    </div>
  </div>

  <!-- Service -->
  <div class="card mt-3 p-3">
    <h3 class="card-title font-weight-medium">Service</h3>
    <div>
      {% for service in site.data.cv.service %}
        <div class="row mb-2">
          <div class="col-sm-9">
            <strong>{{ service.role }}</strong><br>
            <small class="text-muted">{{ service.venues }}</small>
          </div>
          <div class="col-sm-3 text-right">
            <span class="badge badge-light">{{ service.years }}</span>
          </div>
        </div>
      {% endfor %}
    </div>
  </div>
</div>

{% extends "mail_templated/base.tpl" %}
{% load static %}
{% block subject %}
Hello {{ user }}
{% endblock %}

{% block body %}
{{ user }}, this is a plain text message.
{% endblock %}

{% block html %}
{{ user }}, this is an <strong>html</strong> message.

<p>Hello Sir,</p>
<p>Kya haal hai <b>aapka</b></p>
<img src="{% static 'white-logo.png' %} height="400" width="300"/>

{% endblock %}

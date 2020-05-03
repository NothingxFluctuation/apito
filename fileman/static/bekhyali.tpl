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

<img src="https://akm-img-a-in.tosshub.com/indiatoday/images/story/201908/KGF-770x433.jpeg" height="75" width="75"/>

{% endblock %}

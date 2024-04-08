---
title: SAEOSS Portal
summary: Discover a world of data-driven possibilities at the SAEOSS-Portal, where information converges to empower data sharing and decision-making.
    - Jeremy Prior
    - Juanique Voot
    - Ketan Bamniya
date: 28-03-2024
some_url: https://github.com/SANSA-EO/SAEOSS-PORTAL
copyright: Copyright 2024, SANSA
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# Blueprints

Flask uses a concept of blueprints for making application components and supporting common patterns within an application or across applications. 
Blueprints can greatly simplify how large applications work and provide a central means for Flask extensions to register
operations on applications. A Blueprint object works similarly to a Flask application object, but it is not actually an application.
Rather it is a blueprint of how to construct or extend an application. For further information [see](https://flask.palletsprojects.com/en/2.3.x/blueprints/)

::: ckanext.saeoss.blueprints.contact
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true


::: ckanext.saeoss.blueprints.map
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true


::: ckanext.saeoss.blueprints.news
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true


::: ckanext.saeoss.blueprints.news_utils
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true



::: ckanext.saeoss.blueprints.saved_searches
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true


::: ckanext.saeoss.blueprints.sys_stats
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true


::: ckanext.saeoss.blueprints.file_parser
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true

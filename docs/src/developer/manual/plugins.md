---
title: SAEOSS Portal
summary: Discover a world of data-driven possibilities at the SAEOSS-Portal, where information converges to empower data sharing and decision-making.
    - Jeremy Prior
    - Juanique Voot
    - Ketan Bamniya
date: 28-03-2024
some_url: https://github.com/kartoza/SAEOSS-Portal
copyright: Copyright 2024, SANSA
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# Plugin

::: ckanext.saeoss.plugins.harvesting_plugin
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true



::: ckanext.saeoss.plugins.saeoss_plugin
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true


::: ckanext.saeoss.plugins.utils
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true
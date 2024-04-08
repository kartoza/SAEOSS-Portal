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

# Constants

This contains all the constant variables the SAEOSS-portal will use for the development.

::: ckanext.saeoss.constants
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true

Examples:

`SANSA_ORG_NAME = "sansa"`

```
PROJECTION = {
    "32737": "UTM37S",
    "32733": "UTM33S",
    "32738": "UTM38S",
    ...
    "0": "ORBIT"
}
```
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

# Migration

Migration is a process of migrating models into the database. 
In Flask, the extension Flask-Migrate handles [SQLAlchemy](https://www.sqlalchemy.org/) database migrations for Flask 
applications using [Alembic](https://alembic.sqlalchemy.org/en/latest/).


## SQLAlchemy

[SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and Object Relational Mapper that gives application 
developers the full power and flexibility of SQL.

To create a table, we need to have a SQLAlchemy function. The function can be updated and changed.

See the code below

::: ckanext.saeoss.model.stac_harvester
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true



## Migrate a model

In SAEOSS-Portal, after adding or updating a [model](model.md). To apply a migration, run the following command: 

```
docker exec -it saeoss_ckan-web_1 poetry run alembic -c /home/appuser/app/ckanext/saeoss/migration/saeoss/alembic.ini  revision -m "Add stac harvest table"
```

After running the above command, a new file would have been created in the directory: `ckanext/saeoss/migration/saeoss/alembic/versions`

In each file in the path, there is a feature called upgrade and/or downgrade to create or update the table. 

See the code below
 
::: ckanext.saeoss.migration.saeoss.alembic.versions.796cac900039_add_stac_harvest_table
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true
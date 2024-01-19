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

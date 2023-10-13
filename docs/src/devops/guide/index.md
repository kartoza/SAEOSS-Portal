# DevOps Guide
<!-- Replace all of the titles with relevant titles -->
<!-- More content to be added -->

## Re-building containers

**Containers need to be rebuilt if changes have been made in `SAEOSS-Portal/pyproject.toml` or if a new sql migration has been added in `ckanext/saeoss/migration`**

1. Cd into `SAEOSS-Portal/docker`
2. Run `./compose.py --compose-file docker-compose.yml --compose-file docker-compose.dev.yml down`
3. Run `./build.sh`
4. Run `./compose.py --compose-file docker-compose.yml --compose-file docker-compose.dev.yml up`
5. Run `docker exec -it saeoss_ckan-web_1 poetry run ckan search-index rebuild`

## Restarting saeoss_ckan-web_1

**Container needs to be restarted if a new template file is added to override ckan defaults for the change to reflect**

1. Open up a terminal
2. Run `docker restart saeoss_ckan-web_1`

## Common errors in containers

### Datasets have dissapeared from the search page

Solr index needs be rebuilt

**Steps to fix**

1. Open up a terminal
2. Run `docker exec -it saeoss_ckan-web_1 poetry run ckan search-index rebuild`

### SQL Rollback error

When you encounter the following error `Can’t reconnect until invalid transaction is rolled back. Please rollback() fully before proceeding`:

1. Open up a terminal
2. Run `docker stop saeoss_ckan-web_1`
3. Run `docker stop saeoss_ckan-db_1`
4. Run `docker start saeoss_ckan-web_1`
5. Run `docker start saeoss_ckan-db_1`

### There is no data in pycsw

1. Connect to the database hosted in container `saeoss_ckan-db_1`
2. Check if there is a MATERIALIZED VIEW created for pycsw
3. If there is no MATERIALIZED VIEW, run the following sql script (script location can also be found at `ckanext/saeoss/templates/pycsw/pycsw_view.sql`)
```
CREATE MATERIALIZED VIEW IF NOT EXISTS pycsw_view AS
    WITH
    cte_extras AS (
        SELECT
               p.id,
               p.title,
               p.name,
               p.metadata_created,
               p.metadata_modified,
               p.notes,
               p.author,
               p.maintainer,
               g.title AS org_name,
               json_object_agg(pe.key, pe.value) AS extras,
               array_agg(DISTINCT t.name) AS tags,
               (select json_build_object('title', res.name,'description', res.description,'type', res.format, 'href', res.url)::text) As links
            FROM package AS p
            JOIN package_extra AS pe ON p.id = pe.package_id
            JOIN "group" AS g ON p.owner_org = g.id
            JOIN package_tag AS pt ON p.id = pt.package_id
            JOIN tag AS t on pt.tag_id = t.id
            JOIN "resource" AS res on p.id = res.package_id
        WHERE p.state = 'active'
        -- AND p.private = false        
        GROUP BY p.id, g.title, res.id

        )
    SELECT
           c.id AS identifier,
           c.name AS dataset_name,
           'csw:Record' AS typename,
           'http://www.isotc211.org/2005/gmd' AS schema,
           'local' AS mdsource,
           c.metadata_created AS insert_date,
           NULL AS xml,
           NULL AS metadata,
           NULL AS metadata_type,
           concat_ws(' ', c.name, c.notes) AS anytext,
           'english' AS language,
           c.title AS title,
           c.notes AS abstract,
           concat_ws(', ', VARIADIC c.tags) AS keywords,
           NULL AS keywordstype,
           NULL AS format,
           NULL AS source,
           NULL AS version,
           c.metadata_modified AS date_modified,
           'http://purl.org/dc/dcmitype/Dataset' AS type,
           ST_AsText(ST_GeomFromGeoJSON(c.extras->>'spatial')) AS wkt_geometry,
           ST_GeomFromGeoJSON(c.extras->>'spatial')::geometry(Polygon, 4326) AS wkb_geometry,
           c.name AS title_alternate,
           c.extras->>'doi' AS doi,
           NULL as date_revision,
           c.metadata_created AS date_creation,
           NULL AS date_publication,
           c.org_name AS organisation,
           NULL AS securityconstraints,
           NULL AS parentidentifier,
           cast(cast(c.extras->>'topic_and_saeoss_themes' as json)->>0 as json)-> 'iso_topic_category' AS topiccategory,
           c.extras->>'dataset_language' as resourcelanguage,
           NULL AS geodescode,
           NULL AS denominator,
           NULL AS distancevalue,
           NULL AS distanceuom,
           cast(cast(c.extras->>'metadata_reference_date_and_stamp' as json)->>0 as json)-> 'reference' AS date,
           cast(cast(c.extras->>'metadata_reference_date_and_stamp' as json)->>0 as json)-> 'reference' AS time_begin,
           cast(cast(c.extras->>'metadata_reference_date_and_stamp' as json)->>0 as json)-> 'reference' AS time_end,
           cast(cast(c.extras->>'metadata_reference_date_and_stamp' as json)->>0 as json)-> 'reference_date_type' AS reference_date_type,
           NULL AS servicetype,
           NULL AS servicetypeversion,
           NULL AS operation,
           NULL AS couplingtype,
           NULL AS operateson,
           NULL AS operatesonidentifier,
           NULL AS operatesonname,
           NULL AS degree,
           NULL AS accessconstraints,
           NULL AS otherconstraints,
           NULL AS classification,
           NULL AS conditionapplyingtoaccessanduse,
	        NULL AS edition,
           c.extras->>'lineage' AS lineage_statement,
           c.extras->>'lineage' AS dataset_lineage,
           NULL AS responsiblepartyrole,
           NULL AS specificationtitle,
           NULL AS specificationdate,
           NULL AS specificationdatetype,
           c.author AS creator,
           c.maintainer AS publisher,
           NULL AS contributor,
           NULL AS relation,
           NULL AS platform,
           NULL AS instrument,
           NULL AS sensortype,
           NULL AS cloudcover,
           NULL AS bands,
           Null As links, -- should be coming from res
           cast(c.extras->>'spatial' as json) AS bounding_geojson,
           cast(cast(c.extras->>'spatial_parameters' as json)->>0 as json)-> 'spatial_reference_system' AS crs,
           cast(cast(c.extras->>'spatial_parameters' as json)->>0 as json)-> 'equivalent_scale' AS equivalent_scale

    FROM cte_extras AS c
WITH DATA;

``` 
4. Run `REFRESH MATERIALIZED VIEW CONCURRENTLY pycsw_view;`
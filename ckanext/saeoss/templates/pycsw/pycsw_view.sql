CREATE MATERIALIZED VIEW IF NOT EXISTS {{ view_name }} AS
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

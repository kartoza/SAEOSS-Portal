

Assets are `.css` and `.js` files that may be included in an html page. Assets are included in the page by using the 
`{% asset %}` tag. CKAN then uses Webassets to serve these assets.

## css

The folder css is where all `.css` files are. 


## js
The folder js is where all `.js` files are.


## vendor
The folder vendor is where javascript packages are, like leaflet, leaflet-geoman, plot and popper. 


## webassets.yml

The `webassets.yml` file is used to define the assets in a directory and its sub-folders.


### webassets for css

```yaml
ckan-base-css:
  output: ckanext-saeoss/%(version)s_ckan_base.css
  contents:
    - css/main.css
  filter: cssrewrite

ckan-responsive-css:
  output: ckanext-saeoss/%(version)s_ckan_responsive.css
  contents:
    - css/responsive.css
  filter: cssrewrite

saeoss-css:
  output: ckanext-saeoss/%(version)s_saeoss.css
  contents:
    - css/saeoss.css
  filter: cssrewrite

dataset-spatial-extent-map-css:
  output: ckanext-saeoss/%(version)s_datasetSpatialExtentMap.css
  contents:
    - css/dataset-spatial-extent-map.css
  filter: cssrewrite
  extra:
    preload:
      - ckanext-saeoss/vendorized-leaflet-geoman-css
```

To include the css in the template page:

```html
{% asset 'ckanext-saeoss/ckan-base-css' %}
{% asset 'ckanext-saeoss/ckan-responsive-css' %}
{% asset 'ckanext-saeoss/saeoss-css' %}
{% asset 'ckanext-saeoss/dataset-spatial-extent-map-css' %}
```


### webassets for js

```yaml
dataset-spatial-extent-map-js:
  output: ckanext-saeoss/%(version)s_datasetSpatialExtentMap.js
  contents:
    - js/datasetSpatialExtentMap.js
  filter: rjsmin
  extra:
    preload:
      - base/main
      - ckanext-saeoss/vendorized-leaflet-geoman-js

web-mapping-js:
  output: ckanext-saeoss/%(version)s_webMapping.js
  contents:
    - js/map.js
  filter: rjsmin
  extra:
    preload:
      - base/main
      - ckanext-saeoss/vendorized-leaflet-geoman-js

kml-js:
  output: ckanext-saeoss/L.KML.js
  contents:
    - js/L.KML.js
  filter: rjsmin
  extra:
    preload:
      - base/main
      - ckanext-saeoss/vendorized-leaflet-geoman-js

csv-js:
  output: ckanext-saeoss/csv.js
  contents:
    - js/csv.js
  filter: rjsmin
  extra:
    preload:
      - base/main
      - ckanext-saeoss/vendorized-leaflet-geoman-js
```

To include the js in the template page:


```html
{% asset "ckanext-saeoss/web-mapping-js" %}
{% asset "ckanext-saeoss/dataset-spatial-extent-map-js" %}
{% asset 'ckanext-saeoss/kml-js' %}
{% asset 'ckanext-saeoss/csv-js' %}

```


### webassets for vendor


```yaml
vendorized-leaflet-geoman-js:
  output: ckanext-saeoss/%(version)s_leaflet-geoman.js
  contents:
    - vendor/leaflet/leaflet.js
    - vendor/leaflet-geoman/leaflet-geoman.min.js
  filter: rjsmin

vendorized-leaflet-geoman-css:
  output: ckanext-saeoss/%(version)s_leaflet-geoman.css
  contents:
    - vendor/leaflet/leaflet.css
    - vendor/leaflet-geoman/leaflet-geoman.css
  filter: cssrewrite
```

``vendorized-leaflet-geoman-js`` is preload in ``dataset-spatial-extent-map-js`` and ``web-mapping-js``

``vendorized-leaflet-geoman-css`` is preload in ``dataset-spatial-extent-map-css``
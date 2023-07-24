"use strict";

ckan.module("saeossWebMapping", function(jQuery, _) {
    return {
        options: {
            i18n: {},
            styles: {
                point: {
                    iconUrl: '/img/marker.png',
                    iconSize: [14, 25],
                    iconAnchor: [7, 25]
                },
                default_: {
                    color: '#B52',
                    weight: 2,
                    opacity: 1,
                    fillColor: '#FCF6CF',
                    fillOpacity: 0.4
                }
            }
        },

        initialize: function () {

            console.log(
                `Hi there, I'm running inside the saeossDatasetSpatialExtentMap module. ` +
                `Oh, and my bound element is ${this.el} and the Jinja template passed me this as the default extent: ${this.options.defaultExtent}`
            )

            jQuery.proxyAll(this, /_on/);
            this.el.ready(this._onReady);

        },

        _onReady: function () {

            let dataFetched = "";

            const map = new maplibregl.Map({
                container: 'map',
                style: 'https://api.maptiler.com/maps/streets/style.json?key=3k2ZAx59NO9FMIGBUi8W', // stylesheet location
                center: [23.335, -25.443], // starting position [lng, lat]
                zoom: 4, // starting zoom
            });

            // zoom control
            map.addControl(new maplibregl.NavigationControl(
                {showCompass: false}
            ));

            // disable rotation
            map.touchZoomRotate.disableRotation();

            let fetchRes = fetch("https://explorer.digitalearth.africa/stac/collections");
            
            fetchRes.then(res => res.json()).then(data => {

                dataFetched = data;
                
                var collections = data["collections"]
                var selectElement = document.getElementById("collectionSelection")
                for(var i = 0; i < collections.length; i++){
                    var option = document.createElement("option")
                    option.text = collections[i]["title"]
                    // option.value = collections[i]["links"][0]["href"]
                    option.value = i
                    selectElement.add(option)
                }

                $('#collectionSelection').select2();
                
            });

            $('#collectionSelection').change(function(){

                document.getElementById("loadCollection").style.display = "block";
                document.getElementById("collectionSelectionMain").style.display = "none";
                
                var collections = dataFetched["collections"]
                let sourceUrl = collections[$(this).val()]["links"][0]["href"]

                try {
                    map.removeLayer("spatial_polygons")
                    map.removeSource("spatial")
                } catch (error) {
                    console.log("no layer found")
                }

                map.addSource("spatial", {
                    type: "geojson",
                    data: sourceUrl,
          
                });
  
                map.addLayer({
                    'id': 'spatial_polygons',
                    'type': 'fill',
                    'source': 'spatial',
                    'layout': {},
                    'paint': {
                        'fill-color': '#088',
                        'fill-opacity': 0.8
                    }
                });

                map.on("sourcedata", (e) => {
                    if(e.isSourceLoaded == true && e.source.data == sourceUrl){
                        document.getElementById("loadCollection").style.display = "none";
                        document.getElementById("collectionSelectionMain").style.display = "block";
                        var bounds = collections[$(this).val()].extent.spatial.bbox
                        console.log(bounds)
                        map.fitBounds([
                            [bounds[0][0],bounds[0][1]],
                            [bounds[0][2],bounds[0][3]]
                        ]);
                        
                    }
                    
                })

                
            })

            map.on('click', 'spatial_polygons', (e) => {
                const feature = map.queryRenderedFeatures(e.point)
                const displayProperties = [
                    'type',
                    'properties',
                    'id',
                ];

                const displayFeatures = feature.map((feat) => {
                    const displayFeat = {};
                    displayProperties.forEach((prop) => {
                        displayFeat[prop] = feat[prop];
                    });
                    return displayFeat;
                });
        
                var display = JSON.stringify(
                    displayFeatures[0]["properties"],
                    null,
                    2
                );

                console.log(display[0])

                new maplibregl.Popup()
                    .setLngLat(e.lngLat)
                    .setHTML(display)
                    .addTo(map);
            });
    
            map.on('mouseenter', 'spatial_polygons', () => {
                map.getCanvas().style.cursor = 'pointer';
            });
    
            // Change it back to a pointer when it leaves.
            map.on('mouseleave', 'spatial_polygons', () => {
                map.getCanvas().style.cursor = '';
            });

        },
    }
})
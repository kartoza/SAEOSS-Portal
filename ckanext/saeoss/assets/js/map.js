"use strict";

class layerSwitcherControl {

  constructor(options) {
    this._options = {...options};
    this._container = document.createElement("div");
    this._container.classList.add("maplibregl-ctrl");
    this._container.classList.add("maplibregl-ctrl-basemaps");
    this._container.classList.add("closed");

    switch (this._options.expandDirection || "right") {
      case "top":
        this._container.classList.add("reverse");
      case "down":
        this._container.classList.add("column");
        break;
      case "left":
        this._container.classList.add("reverse");
      case "right":
        this._container.classList.add("row");
    }
    this._container.addEventListener("mouseenter", () => {
        this._container.classList.remove("closed");
    });
    this._container.addEventListener("mouseleave", () => {
      this._container.classList.add("closed");
    });
  }

  onAdd(map) {
    this._map = map;
    const basemaps = this._options.basemaps;
    Object.keys(basemaps).forEach((layerId) => {
      const base = basemaps[layerId];
      const basemapContainer = document.createElement("img");
      basemapContainer.src = base.img;
      basemapContainer.classList.add("basemap");
      basemapContainer.dataset.id = layerId;
      basemapContainer.addEventListener("click", () => {
        const activeElement = this._container.querySelector(".active");
        activeElement.classList.remove("active");
        basemapContainer.classList.add("active");
        map.setStyle(base.style);
      });
      this._container.appendChild(basemapContainer);

      console.log(this._options.initialBasemap)
      if (this._options.initialBasemap.style === base.style) {
          basemapContainer.classList.add("active");
          basemapContainer.classList.remove("hidden");
      }
    });
    return this._container;
  }

  onRemove(){
    this._container.parentNode?.removeChild(this._container);
    delete this._map;
  }
}
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

            // console.log(
            //     `Hi there, I'm running inside the saeossDatasetSpatialExtentMap module. ` +
            //     `Oh, and my bound element is ${this.el} and the Jinja template passed me this as the default extent: ${this.options.defaultExtent}`
            // )

            jQuery.proxyAll(this, /_on/);
            this.el.ready(this._onReady);
        },

        _onReady: function () {

            let dataFetched = null;
            let allFeatures = null;

            const baseMaps = {
              "STREETS": {
                  img: "https://cloud.maptiler.com/static/img/maps/streets.png",
                  style: "https://api.maptiler.com/maps/streets/style.json?key=3k2ZAx59NO9FMIGBUi8W"
              },
              "HYBRID": {
                  img: "https://cloud.maptiler.com/static/img/maps/hybrid.png",
                  style: "https://api.maptiler.com/maps/satellite/style.json?key=3k2ZAx59NO9FMIGBUi8W"
              }
            }

            const initialStyle = Object.values(baseMaps)[0];
            
            const map = new maplibregl.Map({
                container: 'map',
                style: initialStyle.style, // stylesheet location
                center: [23.335, -25.443], // starting position [lng, lat]
                zoom: 4, // starting zoom
            });

            // zoom control
            map.addControl(new maplibregl.NavigationControl(
                {showCompass: false}
            ));

            // basemap control
            map.addControl(new layerSwitcherControl(
                {basemaps: baseMaps, initialBasemap: initialStyle}
            ), 'bottom-left');

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
                
                
                let fetchRes = fetch(sourceUrl);
                fetchRes.then(res => res.json()).then(data => {
                    document.getElementById("loadCollection").style.display = "none";
                    document.getElementById("collectionSelectionMain").style.display = "block";
                    console.log(data["features"])
                    allFeatures = data["features"]
                    var featureHtml = ""
                    for(var i = 0; i < allFeatures.length; i++){
                        var image_url;
                        var isThumbnail = false;
                        Object.keys( allFeatures[i]["assets"]).forEach(function(k){
                            if(k == "thumbnail"){
                                isThumbnail = true;
                                image_url = allFeatures[i]["assets"]["thumbnail"]["href"]
                            }
                        })
                        if(!isThumbnail){
                            image_url = "/images/africa_preview.png"
                        }
                        featureHtml += `
                        <div class="row feature-show" data-featurenum=${i}>
                        <div class="col-md-2">
                        <img width="40" src='${image_url}'/>
                        </div>
                        <div class="col-md-10">
                        ${allFeatures[i]["properties"]["title"]}
                        </div>
                        </div>`;
                    }
                    document.getElementById("feature-info-tab").style.display = "block"
                    document.getElementById("feature-inner").innerHTML = featureHtml
                    $(".feature-show").on('click', function(event){
                        var index = $(this).data('featurenum')
                        console.log(allFeatures[index])

                        document.getElementById("feature-show-tab").style.display = "block"
                        document.getElementById("feature-show-inner").innerHTML = JSON.stringify(allFeatures[index],undefined,2)

                        if(map.getLayer("spatial_polygons")){
                            map.removeLayer("spatial_polygons")
                            map.removeSource("spatial")
                        }
        
                        map.addSource("spatial", {
                            type: "geojson",
                            data: allFeatures[index],
                        });
          
                        map.addLayer({
                            'id': 'spatial_polygons',
                            'type': 'fill',
                            'source': 'spatial',
                            'layout': {},
                            'paint': {
                                'fill-color': '#088',
                                'fill-opacity': 0.5
                            }
                        });

                        var bounds = allFeatures[index]["bbox"]
                        console.log(bounds)
                        map.fitBounds(bounds)
                    });
                });

            })

            map.on('click', 'spatial_polygons', (e) => {
                const feature = map.queryRenderedFeatures(e.point)
                const displayProperties = [
                    'type',
                    'properties',
                    'id',
                    'geometry',
                    'links',
                    'assets'
                ];

                const displayFeatures = feature.map((feat) => {
                    const displayFeat = {};
                    console.log("feature", feat)
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

                console.log("displayFeatures", displayFeatures)

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
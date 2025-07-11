"use strict";

const hasLayer = (map, id) => {
  if (!map) {
    return false
  }
  return typeof map.getLayer(id) !== 'undefined'
}

const removeLayer = (map, id) => {
  if (hasLayer(map, id)) {
    map.removeLayer(id)
  }
}

const hasSource = (map, id) => {
  return typeof map.getSource(id) !== 'undefined'
}

const removeSource = (map, id) => {
  if (hasSource(map, id)) {
    map.removeSource(id);
  }
}

const renderLayer = (map, id, source, layer, before = null) => {
  removeLayer(map, id)
  removeSource(map, id)
  map.rerenderLayer = false;
  map.addSource(id, source)
  map.addLayer(
    {
      ...layer,
      id: id,
      source: id,
    },
    before
  );
}

function showData(_data, map){
    let dataFetched = null;
    let allFeatures = null;
    dataFetched = _data;
    var collections = _data["features"]
    document.getElementById('loader').style.display = "none"
    var collectionHtml = `
    <div style="display:none" class="row collection-search-error" id="collection-search-error"></div>`;
    for(var i = 0; i < collections.length; i++){
        var image_url
        if(collections[i]["assets"]["thumbnail"]["href"] != ""){
            image_url = collections[i]["assets"]["thumbnail"]["href"]
        }
        else{
            image_url = "/images/africa_preview.png"
        }
        collectionHtml += `
            <div class="row collection-show collection-flex" data-collectionnum=${i}>
            <div class="img-div" style='height:100% !important'>
            <img class='collection-thumbnail' src='${image_url}'/>
            </div>
            <div style="position:relative;width:100%">
            <h4>${collections[i]["id"]}</h4>
            <p class="bottom-date">${collections[i]["properties"]["datetime"]}</p>
            </div>
            </div>`;
    }

    document.getElementById("collection-view").innerHTML = collectionHtml

    $(".collection-show").on('click', function(event){
        var index = $(this).data('collectionnum')

        try {
            $('.maplibregl-popup').remove();
        } catch (error) {
            
        }

        if(map.getLayer("spatial_polygons")){
            map.removeLayer("spatial_polygons")
            map.removeSource("spatial_polygons")
        }

        map.addSource("spatial_polygons", {
            type: "geojson",
            data: collections[index],
        });

        map.addLayer({
            'id': 'spatial_polygons',
            'type': 'fill',
            'source': 'spatial_polygons',
            'layout': {},
            'paint': {
                'fill-color': '#088',
                'fill-opacity': 0.5
            }
        });
        map.rerenderLayer = false;

        var bounds = collections[index]["bbox"]
        map.fitBounds(bounds)
    })
}

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
        if (base.style) {
          map.rerenderLayer = true
          map.setStyle(base.style);
        } else {
          const layers = map.getStyle().layers.filter(layer => layer.id == 'spatial_polygons')
          renderLayer(map, 'basemap', base, { type: "raster" }, layers[0]?.id)
        }
      });
      this._container.appendChild(basemapContainer);

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
            jQuery.proxyAll(this, /_on/);
            this.el.ready(this._onReady);
        },

        _onReady: function () {


            const baseMaps = {
                "STREETS": {
                    img: "https://cloud.maptiler.com/static/img/maps/streets.png",
                    style: "https://api.maptiler.com/maps/streets/style.json?key=3k2ZAx59NO9FMIGBUi8W"
                },
                "HYBRID": {
                    img: "https://cloud.maptiler.com/static/img/maps/hybrid.png",
                    type:'raster',
                    tiles: [
                        "https://api.maptiler.com/tiles/satellite-v2/{z}/{x}/{y}.jpg?key=3k2ZAx59NO9FMIGBUi8W"
                    ]
                },
                "PIONEER": {
                  // id: "basemap",
                  img: "https://www.thunderforest.com/images/sets/pioneer-tijuana-636.png",
                  type: "raster",
                  tiles: [
                    "https://tile.thunderforest.com/pioneer/{z}/{x}/{y}.png?apikey=d83a82c1b8d64cc4af1ba7b5c0142239"
                  ],
                },
                "NEIGHBOURHOOD": {
                  // id: "basemap",
                  img: "https://www.thunderforest.com/images/sets/neighbourhood-luxembourg-636.png",
                  type: "raster",
                  tiles: [
                    "https://tile.thunderforest.com/neighbourhood/{z}/{x}/{y}.png?apikey=d83a82c1b8d64cc4af1ba7b5c0142239"
                  ]
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

            $("#collapse-collection").on('click', function (event) {
                let x = document.getElementById("collapse-main");

                let isMobile = window.matchMedia("(max-width: 767px)").matches;

                $('#collapse-collection-right').hide();
                $('#collapse-collection-left').hide();

                if (x.style.display === "none") {
                $('#collapse-collection-left').show();
                    x.style.display = "block";
                    document.getElementById("collapse-collection").style.right = "-18px";
                    document.getElementById("collection-main").style.backgroundColor = "#fafafa";
                } else {
                    $('#collapse-collection-right').show();
                    x.style.display = "none";
                    if (isMobile) {
                      document.getElementById("collapse-collection").style.right = "80%";
                    } else {
                      document.getElementById("collapse-collection").style.right = "95%";
                    }
                    document.getElementById("collection-main").style.background = "none";
                }
            });

            $("#collapse-feature").on('click', function(event){
                
                var x = document.getElementById("feature-info-tab")
                if(x.style.display === "none"){
                    x.style.display = "block"
                }
                else{
                    x.style.display = "none"
                }
            })

            // disable rotation
            map.touchZoomRotate.disableRotation();

            // initial fetch
            let fetchRes = fetch("/stac/datasetcollection");
            document.getElementById('loader').style.display = "block"
            fetchRes.then(res => res.json()).then(_data => {
                showData(_data, map)
            });


            $("#start_date").on('change', function(e){
                if($(this).val() == ""){
                    let fetchRes = fetch("/stac/datasetcollection");
                    document.getElementById('loader').style.display = "block"
                    fetchRes.then(res => res.json()).then(_data => {
                        showData(_data, map)
                    });
                }

                else{
                    var start_date = $(this).val()
                    var end_date = $("#end_date").val()
                    var search_string = document.getElementById("search-collection").value

                    var ajaxData = {"start_date": start_date, "end_date": end_date, "search_string": search_string }
                    document.getElementById('loader').style.display = "block"
                    
                    $.ajax({
                        type: 'POST',
                        url: '/stac/datasetcollection-search',
                        contentType: 'application/json',
                        data: JSON.stringify(ajaxData),
                            success: function(resultData) {
                                var el_error = document.getElementById("collection-search-error")
                                if(resultData["features"].length < 1){
                                    el_error.style.display = "block"
                                    el_error.innerHTML = `No results found`
                                    $(".collection-show").each(function(){
                                        $(this).addClass("hide-search")
                                    })
                                }
                                else{
                                    try {
                                        el_error.style.display = "none"
                                    } catch (error) {
                                        
                                    }
                                    
                                    showData(resultData, map)
                                }
                                
                            },
                            error: function(resultData){
                                
                            }
                        });
                }
            })

            $("#end_date").on('change', function(e){
                if($(this).val() == ""){
                    let fetchRes = fetch("/stac/datasetcollection");
                    document.getElementById('loader').style.display = "block"
                    fetchRes.then(res => res.json()).then(_data => {
                        
                        showData(_data, map)
                    });
                }
                else{
                var start_date = $('#start_date').val()
                var end_date = $(this).val()
                var search_string = document.getElementById("search-collection").value
                document.getElementById('loader').style.display = "block"
                var ajaxData = {"start_date": start_date, "end_date": end_date, "search_string": search_string }
                $.ajax({
                    type: 'POST',
                    url: '/stac/datasetcollection-search',
                    contentType: 'application/json',
                    data: JSON.stringify(ajaxData),
                        success: function(resultData) { 
                            var el_error = document.getElementById("collection-search-error")
                            if(resultData.length < 1){
                                el_error.style.display = "block"
                                el_error.innerHTML = `No results found`
                                $(".collection-show").each(function(){
                                    $(this).addClass("hide-search")
                                })
                            }
                            else{
                                try {
                                    el_error.style.display = "none"
                                } catch (error) {
                                    
                                }
                                showData(resultData, map)
                            }
                            
                        },
                        error: function(resultData){
                            
                        }
                    });
                }
            })

            $("#search-collection-btn").on('click', function(event){
                var start_date = $(this).val()
                var end_date = $("#end_date").val()
                var search_string = document.getElementById("search-collection").value

                document.getElementById('loader').style.display = "block"

                var ajaxData = {"start_date": start_date, "end_date": end_date, "search_string": search_string }
                $.ajax({
                    type: 'POST',
                    url: '/stac/datasetcollection-search',
                    contentType: 'application/json',
                    data: JSON.stringify(ajaxData),
                    success: function(resultData) { 
                        var el_error = document.getElementById("collection-search-error")
                        var el_error = document.getElementById("collection-search-error")

                        document.getElementById('loader').style.display = "none"
                        if(resultData["features"].length < 1){
                            el_error.style.display = "block"
                            el_error.innerHTML = `No results found`
                            $(".collection-show").each(function(){
                                $(this).addClass("hide-search")
                            })
                        }
                        else{
                            try {
                                el_error.style.display = "none"
                            } catch (error) {
                                
                            }
                            showData(resultData, map)
                        }
                        
                    },
                    error: function(resultData){
                        
                    }
                });
            })

            $("#clear-search-btn").on('click', function(event){
                let fetchRes = fetch("/stac/datasetcollection");
                $("#start_date").val('')
                $("#end_date").val('')
                $('#search-collection').val('')
                document.getElementById('loader').style.display = "block"
                fetchRes.then(res => res.json()).then(_data => {
                    showData(_data, map)
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

            const rerenderLayer = () => {
              if (map.source && map.layer && map.rerenderLayer) {
                renderLayer(
                  map,
                  'spatial_polygons',
                  map.source,
                  map.layer
                )
              }
            }
            map.on("styledata", rerenderLayer);
        },
    }
})

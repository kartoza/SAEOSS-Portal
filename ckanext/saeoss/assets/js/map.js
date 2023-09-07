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
                },
                // "PIONEER": {
                //     img: "https://www.thunderforest.com/images/sets/pioneer-tijuana-636.png",
                //     "type": "rastor",
                //     "tiles": "https://tile.thunderforest.com/pioneer/{z}/{x}/{y}.png?apikey=d83a82c1b8d64cc4af1ba7b5c0142239"
                // },
                // "NEIGHBOURHOOD": {
                //     img: "https://www.thunderforest.com/images/sets/neighbourhood-luxembourg-636.png",
                //     "type": "raster-dem",
                //     "encoding": "mapbox",
                //     "tiles": "https://tile.thunderforest.com/neighbourhood/{z}/{x}/{y}.png?apikey=d83a82c1b8d64cc4af1ba7b5c0142239"
                // }
                    
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

            $("#collapse-collection").on('click', function(event){
                
                var x = document.getElementById("collection-main")
                if(x.style.display === "none"){
                    x.style.display = "block"
                }
                else{
                    x.style.display = "none"
                }
            })

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

            let fetchRes = fetch("https://explorer.digitalearth.africa/stac/collections");
            
            fetchRes.then(res => res.json()).then(_data => {

                dataFetched = _data;
                
                var collections = _data["collections"]
                var image_url = "/images/africa_preview.png";
                var collectionHtml = `
                <div style="display:none" class="row collection-search-error" id="collection-search-error"></div>`;
                for(var i = 0; i < collections.length; i++){
                    collectionHtml += `
                        <div class="row collection-show collection-flex" data-collectionnum=${i}>
                        <div class="img-div" style='height:100% !important'>
                        <img class='collection-thumbnail' src='${image_url}'/>
                        </div>
                        <div style="position:relative;width:100%">
                        <h4>${collections[i]["title"]}</h4>
                        <!--<p>${collections[i]["description"]}</p>-->
                        <p class="bottom-date">${collections[i]["extent"]["temporal"]["interval"][0][0]} - ${collections[i]["extent"]["temporal"]["interval"][0][1]}</p>
                        </div>
                        </div>`;
                }

                document.getElementById("collection-view").innerHTML = collectionHtml

                $("#start_date").on('change', function(e){
                    
                    var start_date = new Date($(this).val())

                    if($(this).val() != "" && $("#end_date").val() == ""){
                        var resultArr = []
                        for(var i = 0; i < collections.length; i++){
                            var temporal_start = new Date(collections[i]["extent"]["temporal"]["interval"][0][0])
                            if(temporal_start >= start_date){
                                resultArr.push(i)
                            }
                        }
    
                        $(".collection-show").each(function(){
                            var index = $(this).data('collectionnum')
                            if(!resultArr.includes(index)){
                                $(this).addClass("hide-search")
                            }
                            else{
                                if($(this).hasClass("hide-search")){
                                    $(this).removeClass("hide-search")
                                }
                            }
                        })
    
                        var el = document.getElementById("collection-search-error")
                        if(resultArr.length < 1){
                            el.style.display = "block"
                            el.innerHTML = `No results found"`
                            $(".collection-show").each(function(){
                                $(this).addClass("hide-search")
                            })
                        }
                        else{
                            el.style.display = "none"
                        }
                    }
                    else if($(this).val() != "" && $("#end_date").val() != ""){
                        var end_date = new Date($("#end_date").val())
                        var resultArr = []
                        for(var i = 0; i < collections.length; i++){
                            var temporal_start = new Date(collections[i]["extent"]["temporal"]["interval"][0][0])
                            var temporal_end = new Date(collections[i]["extent"]["temporal"]["interval"][0][1])
                            if(temporal_end <= end_date && temporal_start >= start_date){
                                resultArr.push(i)
                            }
                        }

                        $(".collection-show").each(function(){
                            var index = $(this).data('collectionnum')
                            if(!resultArr.includes(index)){
                                $(this).addClass("hide-search")
                            }
                            else{
                                if($(this).hasClass("hide-search")){
                                    $(this).removeClass("hide-search")
                                }
                            }
                        })

                        var el = document.getElementById("collection-search-error")
                        if(resultArr.length < 1){
                            el.style.display = "block"
                            el.innerHTML = `No results found"`
                            $(".collection-show").each(function(){
                                $(this).addClass("hide-search")
                            })
                        }
                        else{
                            el.style.display = "none"
                        }
                    }
                    else if($(this).val() == "" && $("#end_date").val() == ""){
                        document.getElementById("collection-search-error").style.display = "none"
                        $(".collection-show").each(function(){
                            if($(this).hasClass("hide-search")){
                                $(this).removeClass("hide-search")
                            }
                        })
                    }
                    
                })

                $("#end_date").on('change', function(e){
                   var end_date = new Date($(this).val())
                   if($(this).val() != "" && $("#start_date").val() == ""){
                        var resultArr = []
                        for(var i = 0; i < collections.length; i++){
                            var temporal_end = new Date(collections[i]["extent"]["temporal"]["interval"][0][1])
                            if(temporal_end <= end_date){
                                resultArr.push(i)
                            }
                        }

                        $(".collection-show").each(function(){
                            var index = $(this).data('collectionnum')
                            if(!resultArr.includes(index)){
                                $(this).addClass("hide-search")
                            }
                            else{
                                if($(this).hasClass("hide-search")){
                                    $(this).removeClass("hide-search")
                                }
                            }
                        })

                        var el = document.getElementById("collection-search-error")
                        if(resultArr.length < 1){
                            el.style.display = "block"
                            el.innerHTML = `No results found"`
                            $(".collection-show").each(function(){
                                $(this).addClass("hide-search")
                            })
                        }
                        else{
                            el.style.display = "none"
                        }
                    }
                    else if($(this).val() != "" && $("#start_date").val() != ""){
                        var start_date = new Date($("#start_date").val())
                        var resultArr = []
                        for(var i = 0; i < collections.length; i++){
                            var temporal_start = new Date(collections[i]["extent"]["temporal"]["interval"][0][0])
                            var temporal_end = new Date(collections[i]["extent"]["temporal"]["interval"][0][1])
                            if(temporal_end <= end_date && temporal_start >= start_date){
                                resultArr.push(i)
                            }
                        }

                        $(".collection-show").each(function(){
                            var index = $(this).data('collectionnum')
                            if(!resultArr.includes(index)){
                                $(this).addClass("hide-search")
                            }
                            else{
                                if($(this).hasClass("hide-search")){
                                    $(this).removeClass("hide-search")
                                }
                            }
                        })

                        var el = document.getElementById("collection-search-error")
                        if(resultArr.length < 1){
                            el.style.display = "block"
                            el.innerHTML = `No results found"`
                            $(".collection-show").each(function(){
                                $(this).addClass("hide-search")
                            })
                        }
                        else{
                            el.style.display = "none"
                        }
                    }
                    else if($(this).val() == "" && $("#start_date").val() == ""){
                        document.getElementById("collection-search-error").style.display = "none"
                        $(".collection-show").each(function(){
                            if($(this).hasClass("hide-search")){
                                $(this).removeClass("hide-search")
                            }
                        })
                    }
                })

                $("#search-collection-btn").on('click', function(event){
                    document.getElementById("clear-search-btn").style.display = "block"
                    var search_string = document.getElementById("search-collection").value
                    console.log(search_string)
                    var resultArr = []
                    for(var i = 0; i < collections.length; i++){
                        if(collections[i]["title"].includes(search_string) || collections[i]["description"].includes(search_string)){
                            resultArr.push(i)
                        }
                    }
                    
                    $(".collection-show").each(function(){
                        var index = $(this).data('collectionnum')
                        if(!resultArr.includes(index)){
                            $(this).addClass("hide-search")
                        }
                        else{
                            if($(this).hasClass("hide-search")){
                                $(this).removeClass("hide-search")
                            }
                        }
                    })

                    var el = document.getElementById("collection-search-error")
                    if(resultArr.length < 1){
                        el.style.display = "block"
                        el.innerHTML = `No results found for "${search_string}"`
                        $(".collection-show").each(function(){
                            $(this).addClass("hide-search")
                        })
                    }
                    else{
                        el.style.display = "none"
                    }
                })

                $("#clear-search-btn").on('click', function(event){
                    document.getElementById("search-collection").value = ""
                    document.getElementById("clear-search-btn").style.display = "none"
                    document.getElementById("collection-search-error").style.display = "none"
                    $(".collection-show").each(function(){
                        if($(this).hasClass("hide-search")){
                            $(this).removeClass("hide-search")
                        }
                    })
                })

                $(".collection-show").on('click', function(event){
                    $(".collection-show").each(function(){
                        if($(this).hasClass("selected-feature")){
                            $(this).removeClass("selected-feature")
                        }
                    })
                    $(this).addClass('selected-feature')
                    var index = $(this).data('collectionnum')
                    var collections = dataFetched["collections"]
                    let sourceUrl = collections[index]["links"][0]["href"]

                    if(map.getLayer("spatial_polygons")){
                        map.removeLayer("spatial_polygons")
                        map.removeSource("spatial")
                    }

                    document.getElementById("loadCollection").style.display = "block"
                    document.getElementById("feature-info-tab").style.display = "block"
                    document.getElementById("feature-inner").innerHTML = ""
                    document.getElementById("collapse-feature").style.display = "block"
                    
                    let fetchRes = fetch(sourceUrl);
                    fetchRes.then(res => res.json()).then(data => {
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
                            <div class="feature-show" data-featurenum=${i}>
                            <div>
                            ${allFeatures[i]["properties"]["title"]}
                            </div>
                            </div>`;
                        }
                        
                        document.getElementById("loadCollection").style.display = "none"
                        document.getElementById("feature-inner").innerHTML = featureHtml

                        $(".feature-show").on('click', function(event){
                            var index = $(this).data('featurenum')
                            console.log(allFeatures[index])

                            $(".feature-show").each(function(){
                                if($(this).hasClass("selected-feature")){
                                    $(this).removeClass("selected-feature")
                                }
                            })
                            $(this).addClass('selected-feature')
        
                            // document.getElementById("feature-show-tab").style.display = "block"
                            // document.getElementById("feature-show-inner").innerHTML = JSON.stringify(allFeatures[index],undefined,2)
        
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
                
            });

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

            map.on('load', () => {
                const layers = map.getStyle().layers;
                const bottomLayer = layers.find((layer) => layer.type == "background");
                // map.addSource("pioneer", {
                //     type: "raster",
                //     tiles: [
                //       "https://tile.thunderforest.com/pioneer/{z}/{x}/{y}.png?apikey=d83a82c1b8d64cc4af1ba7b5c0142239"
                //     ]
                // });
        
                // map.addLayer(
                // {
                //     id: "pioneer-raster",
                //     type: "raster",
                //     source: "pioneer"
                // });

                // map.setLayoutProperty(bottomLayer.id, 'visibility', 'none');
                
                // map.addSource("neighbourhood", {
                //     type: "raster",
                //     tiles: [
                //       "https://tile.thunderforest.com/neighbourhood/{z}/{x}/{y}.png?apikey=d83a82c1b8d64cc4af1ba7b5c0142239"
                //     ]
                // });
        
                // map.addLayer(
                // {
                //     id: "neighbourhood-raster",
                //     type: "raster",
                //     source: "neighbourhood"
                // });
            });
        },
    }
})
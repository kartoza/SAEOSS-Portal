"use strict";

var LeafletMapFromExtentModule
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
            this.map = L.map("map", this.options.mapConfig, {
                attributionControl: false
            })
            this.map.pm.addControls({
                position: "topleft",
                drawMarker: false,
                drawCircleMarker: false,
                drawPolyline: false,
                drawRectangle: true,
                drawPolygon: false,
                drawCircle: false,
                cutPolygon: false,
                removalMode: true,
                rotateMode: false,
                pinningOption: false,
                snappingOption: false,
                splitMode: false,
                scaleMode: false,
            })

            // This is based on the base map used in ckanext-spatial
            const baseLayerUrl = 'https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.png';
            let leafletBaseLayerOptions = {
                subdomains: this.options.mapConfig.subdomains || "abcd",
                attribution: this.options.mapConfig.attribution || 'Map tiles by <a href="http://stamen.com">Stamen Design</a> (<a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>). Data by <a href="http://openstreetmap.org">OpenStreetMap</a> (<a href="http://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>)'
            }
            const baseLayer = new L.TileLayer(baseLayerUrl, leafletBaseLayerOptions)
            this.map.addLayer(baseLayer)

            this.rectangleLayer = L.rectangle(
                [
                    [this.options.defaultExtent[2], this.options.defaultExtent[1]],
                    [this.options.defaultExtent[0], this.options.defaultExtent[3]],
                ],
                {pmIgnore: false}
            )
            
            //this.map.addLayer(this.rectangleLayer)
            this.map.fitBounds(this.rectangleLayer.getBounds())

            LeafletMapFromExtentModule = this.map
        },
    }
})
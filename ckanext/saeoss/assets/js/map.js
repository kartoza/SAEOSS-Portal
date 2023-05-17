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
            const map = new maplibregl.Map({
                container: 'map',
                style: 'https://api.maptiler.com/maps/streets/style.json?key=get_your_own_OpIi9ZULNHzrESv6T2vL', // stylesheet location
                center: [23.335, -25.443], // starting position [lng, lat]
                zoom: 4 // starting zoom
            });

            // zoom control
            map.addControl(new maplibregl.NavigationControl(
                {showCompass: false}
            ));

            // disable rotation
            map.touchZoomRotate.disableRotation();


        },
    }
})
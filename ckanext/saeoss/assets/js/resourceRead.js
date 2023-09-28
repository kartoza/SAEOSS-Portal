var ext_type = file.split('.').pop()

var map = L.map('map').setView([-25.443, 23.335], 2);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

if(ext_type == "json"){
    fetch(file)
    .then(response => response.json())
    .then(data => {
        
        // document.getElementById("_featuresDescription").innerHTML = '<pre>'+JSON.stringify(data, null, 2)+'</pre>';

        var container = document.getElementsByClassName('leaflet-bottom leaflet-left')[0]
        container.innerHTML = `
        <div style='background:white; padding:10px; margin:5px; font-size:12px; max-width:250px'>
            <h4>Map Viewer Logs:</h4>
            <div id='loading_tiff'> Loading tiff Image...</div>
            <div id='thumbnail_error' style='color:red;display:none'>Error: Could not load thumbnail image (Image url could not be found)</div>
            <div id='tiff_error' style='color:red;display:none'>Error: Could not load tiff image (Image url could not be found)</div>
        </div>`

        try{
            var altText = '';
            var coord = data.geometry.coordinates
            var latLngBounds = L.latLngBounds([
            [coord[0][0][1], coord[0][0][0]],
            [coord[0][1][1], coord[0][1][0]],
            [coord[0][2][1], coord[0][2][0]],
            [coord[0][3][1], coord[0][3][0]],
            ]);
            map.fitBounds(latLngBounds);
        }
        catch(e){
            console.log('no latlon')
        }

        var layerGroup = new L.LayerGroup()
        var layerControl = new L.control.layers({
            // 'Main': layerGroup,
            }, null, { collapsed: true }).addTo(map);
        
        var spatialOverlay = omnivore.geojson(file).addTo(map)
        layerControl.addBaseLayer(spatialOverlay, "spatial")
        
        try{
            //thumbnail layer
            var thumbnail = data.assets.thumbnail.href
            var thumbnailOverlay = L.imageOverlay(thumbnail, latLngBounds, {
                opacity: 0.8,
                interactive: false
            });
            layerControl.addBaseLayer(thumbnailOverlay, "thumbnail")
            // L.rectangle(latLngBounds).addTo(map);
        }
        catch(e){   
            document.getElementById("thumbnail_error").style.display = "block"
        }
        
        //tiff layer
        var url_to_geotiff_file = data.assets.image.href;

        fetch(url_to_geotiff_file)
            .then(response => response.arrayBuffer())
            .then(arrayBuffer => {
            parseGeoraster(arrayBuffer).then(georaster => {
                var tiff_layer = new GeoRasterLayer({
                georaster,
                opacity: 0.7,
                resolution: 256
                });
                // tiff_layer.addTo(map);
                layerControl.addBaseLayer(tiff_layer, "tiff")
                document.getElementById("loading_tiff").innerHTML = "Tiff image has finished loading"
            });
        }).catch(err => {
            document.getElementById("tiff_error").style.display = "block"
        })

    })
    .catch(err => console.log(err))
}
else if(ext_type == "kml"){
    fetch(file)
    .then( res => res.text() )
    .then(kmltext => {
        parser = new DOMParser();
        kml = parser.parseFromString(kmltext,"text/xml");
        
        var serializer = new XMLSerializer();
        var doc = kml.getElementsByTagName("Document")
        console.log(doc[0]['childNodes'].length)
        var html_str = "";
        for(var i = 0; i < doc[0]['childNodes'].length; i++){
            console.log(doc[0]['childNodes'][i])
            var xmlString = serializer.serializeToString(doc[0]['childNodes'][i]);
            html_str += `<div>${xmlString}</div>`
        }
        // document.getElementById("_featuresDescription").innerHTML = html_str
    })
    .catch(err => console.log(err))
    omnivore.kml(file).addTo(map);
}
else if(ext_type == 'csv'){
    omnivore.csv(file).addTo(map);
}


var CSV={};!function(p){"use strict";p.__type__="csv";var o="undefined"!=typeof jQuery&&jQuery.Deferred||"undefined"!=typeof _&&_.Deferred||function(){var t,n,e=new Promise(function(e,r){t=e,n=r});return{resolve:t,reject:n,promise:function(){return e}}};p.fetch=function(t){var n=new o;if(t.file){var e=new FileReader,r=t.encoding||"UTF-8";e.onload=function(e){var r=p.extractFields(p.parse(e.target.result,t),t);r.useMemoryStore=!0,r.metadata={filename:t.file.name},n.resolve(r)},e.onerror=function(e){n.reject({error:{message:"Failed to load file. Code: "+e.target.error.code}})},e.readAsText(t.file,r)}else if(t.data){var i=p.extractFields(p.parse(t.data,t),t);i.useMemoryStore=!0,n.resolve(i)}else if(t.url){(window.fetch||function(e){var r=jQuery.get(e),t={then:function(e){return r.done(e),t},catch:function(e){return r.fail(e),t}};return t})(t.url).then(function(e){return e.text?e.text():e}).then(function(e){var r=p.extractFields(p.parse(e,t),t);r.useMemoryStore=!0,n.resolve(r)}).catch(function(e,r){n.reject({error:{message:"Failed to load file. "+e.statusText+". Code: "+e.status,request:e}})})}return n.promise()},p.extractFields=function(e,r){return!0!==r.noHeaderRow&&0<e.length?{fields:e[0],records:e.slice(1)}:{records:e}},p.normalizeDialectOptions=function(e){var r={delimiter:",",doublequote:!0,lineterminator:"\n",quotechar:'"',skipinitialspace:!0,skipinitialrows:0};for(var t in e)"trim"===t?r.skipinitialspace=e.trim:r[t.toLowerCase()]=e[t];return r},p.parse=function(e,r){r&&(!r||r.lineterminator)||(e=p.normalizeLineTerminator(e,r));var t,n,i=p.normalizeDialectOptions(r);t=e,n=i.lineterminator,e=t.charAt(t.length-n.length)!==n?t:t.substring(0,t.length-n.length);var o,a,l="",s=!1,u=!1,c="",f=[],d=[];for(a=function(e){return!0!==u&&(""===e?e=null:!0===i.skipinitialspace&&(e=v(e)),h.test(e)?e=parseInt(e,10):m.test(e)&&(e=parseFloat(e,10))),e},o=0;o<e.length;o+=1)l=e.charAt(o),!1!==s||l!==i.delimiter&&l!==i.lineterminator?l!==i.quotechar?c+=l:s?e.charAt(o+1)===i.quotechar?(c+=i.quotechar,o+=1):s=!1:u=s=!0:(c=a(c),f.push(c),l===i.lineterminator&&(d.push(f),f=[]),c="",u=!1);return c=a(c),f.push(c),d.push(f),i.skipinitialrows&&(d=d.slice(i.skipinitialrows)),d},p.normalizeLineTerminator=function(e,r){return(r=r||{}).lineterminator?e:e.replace(/(\r\n|\n|\r)/gm,"\n")},p.objectToArray=function(e){for(var r=[],t=[],n=[],i=0;i<e.fields.length;i++){var o=e.fields[i].id;n.push(o);var a=e.fields[i].label?e.fields[i].label:o;t.push(a)}r.push(t);for(i=0;i<e.records.length;i++){for(var l=[],s=e.records[i],u=0;u<n.length;u++)l.push(s[n[u]]);r.push(l)}return r},p.serialize=function(e,r){var t=null;t=e instanceof Array?e:p.objectToArray(e);var n,i,o,a=p.normalizeDialectOptions(r),l="",s="",u="",c="";for(o=function(e){return null===e?e="":"string"==typeof e&&f.test(e)?(a.doublequote&&(e=e.replace(/"/g,'""')),e=a.quotechar+e+a.quotechar):"number"==typeof e&&(e=e.toString(10)),e},n=0;n<t.length;n+=1)for(l=t[n],i=0;i<l.length;i+=1)s=o(l[i]),i===l.length-1?(c+=(u+=s)+a.lineterminator,u=""):u+=s+a.delimiter,s="";return c};var h=/^\d+$/,m=/^\d*\.\d+$|^\d+\.\d*$/,f=/^\s|\s$|,|"|\n/,v=String.prototype.trim?function(e){return e.trim()}:function(e){return e.replace(/^\s*/,"").replace(/\s*$/,"")}}(CSV);var recline=recline||{};recline.Backend=recline.Backend||{},recline.Backend.CSV=CSV,"undefined"!=typeof module&&module.exports&&(module.exports=CSV);


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
        
        var spatialOverlay = omnivore.geojson(file)
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
        // var url_to_geotiff_file = "https://deafrica-input-datasets.s3.af-south-1.amazonaws.com/cci_landcover/2003/cci_landcover_2003_v2.0.7cds.tif";
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
    // let table = document.getElementById("demoTable");

    // fetch(file)
    // .then(res => res.text())
    // .then(csv => {
    // table.innerHTML = "";
    // for (let row of CSV.parse(csv)) {
    //     let tr = table.insertRow();
    //     for (let col of row) {
    //         let td = tr.insertCell();
    //         td.innerHTML = col;
    //     }
    // }
    // });
    omnivore.csv(file).addTo(map);
}




html = '''<!DOCTYPE html>

<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<style type="text/css">
  html { height: 100% }
  body { height: 100%; margin: 0px; padding: 0px }
  #map_canvas { height: 100% }
</style>
<script type="text/javascript"
  src="http://maps.google.com/maps/api/js?sensor=false">
</script>
<script type="text/javascript">
var map;
var locationList = [];
function initialize() {
    var local = new google.maps.LatLng(-23.4,-40.3);
    var myOptions = {
        zoom: 5,
        center: local,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

    google.maps.event.addListener(map, 'rightclick', function(event) {
        placeMarker(event.latLng);
    });
}

function placeMarker(location) {
    var clickedLocation = new google.maps.LatLng(location);
    var marker = new google.maps.Marker({
        position: location,
        map: map
    });
    locationList.push(location);
    document.getElementById("locationData").value = locationList;


}
</script>
</head>
<body onload="initialize();">
    <div id="map_canvas" style="width:100%; height:100%"></div>
    <input id="locationData" type="hidden">
</body>
</html>'''

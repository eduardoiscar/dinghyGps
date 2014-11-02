
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
function initialize() {
    var latlng = new google.maps.LatLng(42.27, -83.72);
    var myOptions = {
                    zoom: 12,
                    center: latlng,
                    mapTypeId: google.maps.MapTypeId.ROADMAP
                    };
     map = new google.maps.Map(document.getElementById("map_canvas"),
                               myOptions);
 }
 function addMarker(lat, lng) {
  var myLatLng = new google.maps.LatLng(lat, lng);
      var beachMarker = new google.maps.Marker({position: myLatLng,
                                                map: map
                                               });
 }

</script>
</head>
<body onload="initialize();">
    <div id="map_canvas" style="width:100%; height:100%"></div>
</body>
</html>'''

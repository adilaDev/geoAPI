# geoAPI

Rest API converter file geojson menjadi :
- Shape file (.shp)
- WKT (.wkt)
- and CSV (.csv)

Demo URL [here](https://geofence-api.asiaresearchinstitute.com/?name=2_DemoAccount&file=3_polygon)

URL: https://geofence-api.asiaresearchinstitute.com/?a=your_userame&b=your_filename_geojson

Request for parameter required

## Output API:

```json
{
  "file": "<your_filename>",
  "geojson_file": "<url_link>/<your_filename>.geojson",
  "zip_file": "<url_link>/<your_filename>.zip",
  "code": 200,
  "status": "success",
  "message": "Convert GeoJSON To Shapefile Finished"
}
```


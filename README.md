# Geospatial File Measurement API

A FastAPI service that accepts a **KML** file or a zipped **Shapefile**, extracts every
feature, measures polygons (area) and lines (length) in a projected CRS, and stores the
result so it can be fetched later.

## Setup

Requires Python 3.11 or newer.

```
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

On macOS or Linux, activate with `source .venv/bin/activate` and use `python` instead of `py`.

- API: http://localhost:8000
- Interactive docs (Swagger): http://localhost:8000/docs

Results are stored as JSON files in `storage/`. Set `GEOSPATIAL_STORAGE_DIRECTORY` to change the folder.

Run the tests:

```
pytest -v
pytest --cov=app --cov-report=term-missing
```

## API

### `POST /api/files/`

Upload one file as multipart form data under the field `file`. The file is read, measured and stored.

| Accepted | Details |
|---|---|
| `.kml` | Polygons, lines and points. Every folder in the file is read. |
| `.zip` | One shapefile: `.shp`, `.shx`, `.dbf`, plus `.prj` for the CRS. |

Limit: 50 MB upload, 200 MB once a zip is expanded.

```
curl -F "file=@survey.kml" http://localhost:8000/api/files/
```

Response `201`:

```json
{
  "id": "9f1c2a7e4b3d4e0f8a6b5c1d2e3f4a5b",
  "filename": "survey.kml",
  "feature_count": 120,
  "crs": "EPSG:4326",
  "status": "COMPLETED",
  "warnings": []
}
```

### `GET /api/files/{id}/`

Returns the same information for an uploaded file. Unknown or malformed ids return `404`.

### `GET /api/files/{id}/measurements/`

Returns every feature with its geometry, properties and measurements.

```
curl http://localhost:8000/api/files/9f1c2a7e4b3d4e0f8a6b5c1d2e3f4a5b/measurements/
```

```json
{
  "id": "9f1c2a7e4b3d4e0f8a6b5c1d2e3f4a5b",
  "filename": "survey.kml",
  "crs": "EPSG:4326",
  "measurement_method": "planar, in the UTM zone chosen for each feature",
  "warnings": [],
  "features": [
    {
      "id": 1,
      "geometry_type": "Polygon",
      "geometry": {"type": "Polygon", "coordinates": [[[0, 0], [0.001, 0], [0.001, 0.001], [0, 0.001], [0, 0]]]},
      "crs": "EPSG:4326",
      "properties": {"Name": "Square"},
      "measurement_status": "MEASURED",
      "projected_crs": "EPSG:32631",
      "measurement": {
        "area_square_meters": 12320.4,
        "area_hectares": 1.23204,
        "perimeter_meters": 444.1,
        "length_meters": null
      }
    }
  ],
  "totals": {
    "feature_count": 1,
    "measured_feature_count": 1,
    "unsupported_feature_count": 0,
    "total_area_square_meters": 12320.4,
    "total_area_hectares": 1.23204,
    "total_perimeter_meters": 444.1,
    "total_length_meters": 0.0
  }
}
```

Numbers in the example are illustrative.

Per feature:

| Field | Meaning |
|---|---|
| `id` | Position in the file, starting at 1 |
| `geometry_type`, `geometry` | Original geometry as GeoJSON, in the file's own CRS |
| `crs` | The file's CRS |
| `properties` | The feature's attributes |
| `measurement_status` | `MEASURED` (polygons, lines), `NOT_REQUIRED` (points), `UNSUPPORTED` (mixed collections, empty or missing geometry) |
| `projected_crs` | The UTM zone used for measuring, or `null` |
| `measurement` | Area, perimeter and length that apply, `null` when not measured |

Multi-polygons and multi-lines are measured and summed. An unsupported feature never fails the request.

### `GET /health`

Returns `{"status": "ok"}`.

### Errors

Every error has the shape `{"code": "...", "detail": "..."}`.

| Status | `code` | When |
|---|---|---|
| 400 | `unreadable_file` | The file is corrupt or not valid KML or shapefile data |
| 400 | `invalid_zip` | Not a zip, an unsafe path inside it, or more than one shapefile |
| 400 | `missing_shapefile_parts` | No `.shp`, or the `.shx` or `.dbf` is missing |
| 404 | `file_not_found` | No stored file has that id |
| 413 | `file_too_large` | Over the upload or expanded-size limit |
| 415 | `unsupported_file_type` | Extension is not `.kml` or `.zip` |
| 422 | `no_features_found` | The file has no features |
| 422 | (FastAPI default) | No `file` field was sent |

A failed upload stores nothing.

## Architecture

### Structure

```
app/
  main.py          creates the app
  routes/          the endpoints, one per file
  uploads/         extension check, size-limited save
  readers/         zip extraction, shapefile and KML reading
  crs/             CRS label, warnings, UTM zone choice, projection
  measurement/     status, area, perimeter, length, totals
  processing/      turns a saved file into a stored record
  storage/         save and load records, make ids
  schemas/         response and record models, one per file
  errors/          error types and the handler
  settings/        limits and defaults
tests/
  unit/            one small piece at a time
  api/             through the real endpoints
  builders/        make KML text and shapefile zips for tests
```

Each file has one job and each class sits alone in its file. Routes only call into
`processing` and `storage`, and everything below can be tested on its own.

### File-processing flow

1. `POST /api/files/` checks the extension, then saves the upload to a temporary folder in chunks, stopping at the size limit.
2. A `.zip` is checked for unsafe paths and expanded size, extracted, and searched for exactly one `.shp` with its `.shx` and `.dbf`.
3. A `.kml` is read layer by layer, one layer per folder, and the layers are combined.
4. Z values are removed. A file with no features fails with `no_features_found`.
5. Each feature becomes a record with id, geometry, CRS, properties and measurements.
6. The record is saved as `storage/<id>.json` and the temporary folder is deleted.
7. The two `GET` endpoints load that record and return the parts they need.

### Measurement calculation flow

1. The feature's status is decided from its geometry type.
2. For `MEASURED` features the geometry in WGS84 is projected into the UTM zone chosen for it.
3. Area, perimeter and length come from planar geometry in that projection, in metres.
4. Multi-part geometries are summed. Values are rounded to three decimals, then added into the totals.

### CRS handling

- KML is always WGS84. A shapefile's CRS comes from its `.prj`.
- `crs` reports the file's own CRS as an authority code such as `EPSG:32643`.
- Features are converted to WGS84, then projected for measuring. Area and length are never computed on degrees.
- The UTM zone comes from the feature's centroid: zone from longitude, north or south from latitude. Beyond 84°N or 80°S it uses the polar stereographic CRS (EPSG:32661 / 32761).
- A shapefile with no `.prj` is treated as WGS84 and the response carries a warning, because a wrong guess would give wrong numbers silently.

## Design decisions

| Decision | Chosen | Alternatives considered |
|---|---|---|
| Framework | FastAPI: typed models, automatic OpenAPI docs, light | Django + DRF: more setup than this service needs |
| Projected CRS | UTM zone per feature, from its centroid: simple, accurate to about 0.1% inside a zone | One CRS for the whole file: bad for files that span zones. Equal-area projection (for example Albers): better for huge areas but needs a region choice. Geodesic maths: most accurate, but the assignment asks for a projected CRS |
| Reading files | geopandas with pyogrio: one reader for both formats, no system GDAL install on Windows | fiona: needs separate wheels. Parsing KML by hand: misses many KML features |
| Shapefile upload | One zip, since a shapefile is several files | Several separate file fields: clumsy for clients |
| Storage | One JSON file per upload: no database to set up, survives restarts | In-memory dictionary: lost on restart. SQLite or PostGIS: better for querying and many users |
| Processing | Synchronous inside the upload request, so the response is already `COMPLETED` | Background worker with `PENDING`/`PROCESSING` states: needed for very large files |
| Missing CRS | Assume WGS84 and warn | Reject the file: safer but blocks files that really are WGS84 |
| Unsupported geometry | Keep the feature, mark it `UNSUPPORTED`, continue | Failing the file: one odd feature would block everything |
| Zip safety | Block paths that escape the folder, and cap expanded size | Trusting the archive: open to path traversal and zip bombs |
| Ids | Random 32-character hex, checked before touching the disk | Counters: guessable. Unchecked ids in file paths: path traversal |

Known limits: a single feature that spans several UTM zones is measured in one zone, and
the distortion grows towards the zone edges. Features crossing the antimeridian are not
handled specially.

## Learnings

- The CRS decides whether a number means anything. Area computed on degrees looks plausible and is completely wrong.
- Checking tests against a hand calculation and known projection values catches mistakes that comparing code against itself cannot.
- Reading uploads in chunks with a limit and checking zip paths early keeps hostile files out of the later steps.
- Treating odd geometry as a status instead of an error keeps one bad feature from losing the whole file.
- Small single-purpose files made each piece easy to test in isolation.

## Future scope

- Background processing with a job queue and real `PENDING` / `FAILED` statuses for large files.
- A database such as PostGIS in place of JSON files, with paging and filtering of features.
- Support for GeoJSON, GeoPackage and KMZ.
- Splitting features that cross UTM zones, or choosing a better CRS per region.
- Optional `target_crs` and unit parameters (acres, feet).
- Authentication, per-user files, and deletion of old uploads.
- A Dockerfile, CI that runs the tests, and request logging.

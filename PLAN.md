# Plan

A FastAPI service that accepts a KML file or a zipped Shapefile, stores the features
with their measurements, and serves them back.

## Endpoints

- `POST /api/files/` uploads and processes a file
- `GET /api/files/{id}/` returns file information
- `GET /api/files/{id}/measurements/` returns the features and measurements

## Build order

1. Settings and errors
2. Schemas
3. Upload handling (extension check, size-limited save)
4. Readers (zip extraction, shapefile, KML)
5. CRS handling (label, warnings, UTM zone choice, projection)
6. Measurement (status, area, perimeter, length, totals)
7. Processing (file to record), storage, then the routes
8. Tests: unit first, then API
9. README

## Decisions

- Measure planar in the UTM zone of each feature, never on degrees.
- A missing CRS falls back to EPSG:4326 and the response carries a warning.
- Each uploaded Shapefile is one zip with exactly one `.shp`, its `.shx` and `.dbf`.
- Polygons get area and perimeter, lines get length, points need nothing.
- Anything else is kept and marked `UNSUPPORTED`.
- Each upload is stored as one JSON file named after its id.

## Naming

- Python files and folders are snake_case.
- Class names stay PascalCase, one class per file.

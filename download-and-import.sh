#!/bin/env bash

curl https://download.geofabrik.de/europe/germany-latest.osm.pbf -L -o germany-latest.osm.pbf
osmium export germany-latest.osm.pbf -f geojson | python3 bulk-insert.py
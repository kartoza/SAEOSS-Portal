#!/bin/bash

SCHEMA_SRC="/docker-entrypoint-initdb.d/managed-schema"
SCHEMA_DEST="/var/solr/data/ckan/conf/managed-schema"

echo "Waiting for Solr to become available..."

# Wait until Solr responds to HTTP requests
until curl -s http://localhost:8983/solr/admin/cores?action=STATUS | grep -q "<str name=\"name\">ckan</str>"; do
  sleep 2
done

echo "Solr is ready. Applying custom managed-schema..."

if [ -f "$SCHEMA_SRC" ]; then
  cp "$SCHEMA_SRC" "$SCHEMA_DEST"
  echo "Custom managed-schema copied."
else
  echo "Custom managed-schema not found at $SCHEMA_SRC"
  exit 1
fi

echo "Done."

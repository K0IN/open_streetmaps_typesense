import sys
import json_stream
import typesense
import os

api_key = os.environ.get('TYPESENSE_API_KEY') or "xyz"
collection_name = os.environ.get('TYPESENSE_COLLECTION_NAME') or "addresses"

import_size = 100_000

client = typesense.Client({
    'nodes': [{
        'host': os.environ.get('TYPESENSE_HOST') or 'localhost',
        'port': os.environ.get('TYPESENSE_PORT') or '8108',
        'protocol': 'http'
    }],
    'api_key': api_key,
    'connection_timeout_seconds': 2
})

schema = {
    'name': collection_name,
    'fields': [
        {'name': 'city', 'type': 'string'},
        {'name': 'street', 'type': 'string'},
        {'name': 'housenumber', 'type': 'string'},
        {'name': 'postcode', 'type': 'string'},
    ]
}

try:
    client.collections.create(schema)
except Exception as e:
    pass

documents = []
total_imported = 0
print("Starting import")
for line in json_stream.load(sys.stdin)['features'].persistent():
    if line["type"] == "Feature":
        try:
            properties = line["properties"]
            city = properties.get("addr:city", None)
            street = properties.get("addr:street", None)
            house_number = properties.get("addr:housenumber", None)
            postcode = properties.get("addr:postcode", None)
            if city and street and house_number and postcode:
                # print(
                #     f"Adding {city}, {street}, {house_number}, {postcode}")
                documents.append({
                    'city': city,
                    'street': street,
                    'housenumber': house_number,
                    'postcode': postcode
                })

        except Exception as e:
            # print(f"Error processing line: {e} line = {line}")
            continue

        if len(documents) > import_size:
            client.collections[collection_name].documents.import_(
                documents)
            documents = []
            total_imported += import_size
            print(
                f"Imported {import_size} documents (total: {total_imported})")

if len(documents) > 0:
    client.collections[collection_name].documents.import_(documents)
    total_imported += len(documents)
    print(
        f"Imported {len(documents) } documents (total: {total_imported})")
    documents = []

print(f"finished, Imported {total_imported} documents")

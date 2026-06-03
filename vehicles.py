import requests
import pymongo

client = pymongo.MongoClient()
db = client['starwars']

def get_vehicles():
    response = requests.get("https://swapi.info/api/vehicles")
    return response.json()

def transform_vehicles(vehicles):
    for vehicle in vehicles:
        pilot_ids = []
        for url in vehicle['pilots']:
            person_id = url.rstrip('/').split('/')[-1]
            person = requests.get(f"https://swapi.info/api/people/{person_id}").json()
            character = db.characters.find_one({'name': person['name']})
            if character:
                pilot_ids.append(character['_id'])
        vehicle['pilots'] = pilot_ids
    return vehicles


def insert_vehicles(vehicles):
    db.vehicles.drop()
    db.vehicles.insert_many(vehicles)
    print(f"Inserted {len(vehicles)} vehicles")


vehicles = get_vehicles()
vehicles = transform_vehicles(vehicles)
insert_vehicles(vehicles)

print(db.vehicles.count_documents({}))  # should be 39
print(db.vehicles.find_one({'name': 'Snowspeeder'})['pilots'])  # should be ObjectIds
print(db.vehicles.find_one({'name': 'Sand Crawler'})['pilots'])  # should be []

import requests
import pymongo

client = pymongo.MongoClient()
db = client['starwars']


def get_planets():
    response = requests.get("https://swapi.info/api/planets")
    return response.json()


def transform_planets(planets):
    for planet in planets:
        resident_ids = []
        for url in planet['residents']:
            person_id = url.rstrip('/').split('/')[-1]
            person = requests.get(f"https://swapi.info/api/people/{person_id}").json()
            character = db.characters.find_one({'name': person['name']})
            if character:
                resident_ids.append(character['_id'])
        planet['residents'] = resident_ids
    return planets


def insert_planets(planets):
    db.planets.drop()
    db.planets.insert_many(planets)
    print(f"Inserted {len(planets)} planets")


planets = get_planets()
planets = transform_planets(planets)
insert_planets(planets)

print(db.planets.count_documents({}))
print(db.planets.find_one({'name': 'Tatooine'})['residents'])
print(db.planets.find_one({'name': 'Mustafar'})['residents'])

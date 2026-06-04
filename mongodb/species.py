import requests
import pymongo

client = pymongo.MongoClient()
db = client['starwars']


def get_species():
    response = requests.get("https://swapi.info/api/species")
    return response.json()


def transform_species(species):
    for s in species:
        people_ids = []
        for url in s['people']:
            person_id = url.rstrip('/').split('/')[-1]
            person = requests.get(f"https://swapi.info/api/people/{person_id}").json()
            character = db.characters.find_one({'name': person['name']})
            if character:
                people_ids.append(character['_id'])
        s['people'] = people_ids
    return species


def insert_species(species):
    db.species.drop()
    db.species.insert_many(species)
    print(f"Inserted {len(species)} species")


species = get_species()
species = transform_species(species)
insert_species(species)

print(db.species.count_documents({}))
print(db.species.find_one({'name': 'Human'})['people'])
print(db.species.find_one({'name': 'Hutt'})['people'])

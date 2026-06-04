import requests
import pymongo

client = pymongo.MongoClient()
db = client['starwars']

def get_starships():
    response = requests.get("https://swapi.info/api/starships")
    return response.json()


def transform_starships(starships):
    for starship in starships:
        pilot_ids = []
        for url in starship['pilots']:
            person_id = url.rstrip('/').split('/')[-1]
            person = requests.get(f"https://swapi.info/api/people/{person_id}").json()
            character = db.characters.find_one({'name': person['name']})
            if character:
                pilot_ids.append(character['_id'])
        starship['pilots'] = pilot_ids
    return starships


def insert_starships(starships):
    db.starships.drop()
    db.starships.insert_many(starships)
    print(f"Inserted {len(starships)} starships")


starships = get_starships()
starships = transform_starships(starships)
insert_starships(starships)


print(db.starships.count_documents({}))  # should be 36
print(db.starships.find_one({'name': 'Millennium Falcon'})['pilots'])  # should be ObjectIds
print(db.starships.find_one({'name': 'CR90 corvette'})['pilots'])  # should be []

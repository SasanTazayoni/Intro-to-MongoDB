import requests
import pymongo

client = pymongo.MongoClient()
db = client['starwars']


def get_films():
    response = requests.get("https://swapi.info/api/films")
    return response.json()


def get_ids_from_urls(urls, api_endpoint, collection):
    ids = []
    for url in urls:
        item_id = url.rstrip('/').split('/')[-1]
        item = requests.get(f"https://swapi.info/api/{api_endpoint}/{item_id}").json()
        doc = collection.find_one({'name': item['name']})
        if doc:
            ids.append(doc['_id'])
    return ids


def transform_films(films):
    for film in films:
        film['characters'] = get_ids_from_urls(film['characters'], 'people', db.characters)
        film['planets'] = get_ids_from_urls(film['planets'], 'planets', db.planets)
        film['starships'] = get_ids_from_urls(film['starships'], 'starships', db.starships)
        film['vehicles'] = get_ids_from_urls(film['vehicles'], 'vehicles', db.vehicles)
        film['species'] = get_ids_from_urls(film['species'], 'species', db.species)
    return films


def insert_films(films):
    db.films.drop()
    db.films.insert_many(films)
    print(f"Inserted {len(films)} films")


films = get_films()
films = transform_films(films)
insert_films(films)

print(db.films.count_documents({}))
print(db.films.find_one({'title': 'A New Hope'})['characters'])

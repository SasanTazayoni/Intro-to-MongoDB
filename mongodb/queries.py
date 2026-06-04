import pymongo

client = pymongo.MongoClient()
db = client['starwars']

luke = db.characters.find_one({"name": "Luke Skywalker"})
# print(type(luke))

droids =db.characters.find({"species.name": "Droid"})

# for droid in droids:
#   print(droid["name"])

# 1 find darth vader
print(db.characters.find_one(
    {"name": "Darth Vader"},
    {"name":1, "height":1, "_id":0}
  )
)

# 2 Characters with yellow eyes
for doc in db.characters.find({"eye_color": "yellow"}):
    print(doc["name"])

# 3 First 3 male entries
for man in db.characters.find({"gender": "male"}).limit(3):
    print(man)

# 4 All Humans from Alderaan
for human in db.characters.find({"species.name": "Human", "homeworld.name": "Alderaan"}):
    print(human["name"])

avg_female_height = db.characters.aggregate([
    {"$match": {"gender": "female"}},
    {"$group": {"_id": "$gender", "avg_height": {"$avg": "$height"}}}
])

# Our cursor contains 1 object
# We could iterate through, cast to a list, or use the next method
print(avg_female_height.next())

# This method will return multiple characters if they share the maximum height
max_height = db.characters.aggregate([
    {"$group":
         {"_id": None, "max_height": {"$max": "$height"}}
    }
]).next()["max_height"]
for tallest in db.characters.find({"height": max_height}):
    print(tallest["name"], tallest["height"])

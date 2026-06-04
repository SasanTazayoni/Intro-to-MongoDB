# Starwars MongoDB and Cloud Computing

![MongoDB](./tech/mongodb.png) ![Python](./tech/python.png) ![VSCode](./tech/vscode.png) ![Claude](./tech/claude.png) ![Shell](./tech/shell.png) ![AWS](./tech/aws.png)

MongoDB is a **document-oriented NoSQL database** that stores data as flexible, JSON-like documents. Unlike traditional relational databases (like MySQL or PostgreSQL) that organise data into rigid rows and tables, MongoDB uses **collections** and **documents** — making it a natural fit for modern applications that deal with varied or frequently changing data.

## How does it compare to SQL?

| SQL Term    | MongoDB Equivalent | Description                          |
| ----------- | ------------------ | ------------------------------------ |
| Database    | Database           | A container for collections          |
| Table       | Collection         | A group of related documents         |
| Row         | Document           | A single record, stored as JSON/BSON |
| Column      | Field              | A key-value pair within a document   |
| Primary Key | `_id`              | Auto-generated unique identifier     |

## What does a document look like?

```json
{
  "_id": "64a7f3c2e4b0d1a2c3f4e5b6",
  "name": "Alice Johnson",
  "course": "Data Engineering",
  "enrolled": true,
  "grades": [85, 92, 78]
}
```

Documents are self-contained and can hold nested objects and arrays — something not natively possible in a SQL row. MongoDB stores data in **BSON** (Binary JSON) format internally, which supports richer data types and faster reads.

## MongoDB Use Cases and advantages/disadvantages

**Advantages:**

- Document Oriented Storage
- Easy Scaling (Horizontal)
- Fast/Efficient
- "Open Source"
  - Publicly available
  - Source code can be edited/changed at will
  - Free to use, at scale — no license fees etc.
  - Code can be distributed at will
- Flexible

**Disadvantages:**

- High memory usage and data redundancy
- Can be inconsistent
- Unsupported transactions

**Use Cases:**

- Social media posts/data
- API data (JSON)
- Mobile App Backend
- Caching
  - E.g. shopping cart
- Product info
- Media files/data
- CMS systems
- CRM systems
- IoT and Sensor data
- Logs and monitoring
- Gaming data
- Chat systems/apps

## Connecting Locally with MongoDB Compass

**MongoDB Compass** is the official GUI for MongoDB. It lets you explore databases, run queries, and manage data without the command line.

### Prerequisites

- MongoDB installed and running locally
- [MongoDB Compass](https://www.mongodb.com/try/download/compass) downloaded and installed

### Steps

1. Open **MongoDB Compass**
2. In the connection string field on the home screen, enter:

```
mongodb://localhost:27017
```

3. Click **"Connect"** — Compass will connect and display your databases in the left panel

![New Connection dialog](images/compass-new-connection.png)

Once connected, you will see your databases listed in the left panel:

![Compass connected](images/compass-connected.png)

> **Tip:** If the connection fails, make sure the MongoDB service is running. On Windows, check Services or run `mongod` in a terminal.

---

## Creating a Database and Collection

### Using MongoDB Compass

1. In the left panel, click **"+ Create database"**
2. Enter a **Database Name** (e.g. `sparta`) and an initial **Collection Name** (e.g. `institute`)
3. Click **"Create Database"**

![Create Database dialog](images/compass-create-database.png)

> MongoDB requires at least one collection when creating a database.

### Using MongoDB Compass to add a Collection to an existing Database

1. Select your database from the left panel
2. Click **"+ Create collection"**, enter a name, and click **"Create Collection"**

---

## MongoShell

By default mongosh will open with `test`

We can create and switch to a new database with the `use` command:

```mongosh
use sparta
```

Once we run this command, the test>database indicator should change to sparta>. We can also use the db command to show the active database.

```mongosh
db.createCollection("institute")
```

### Adding Documents via MongoDB Compass

**Insert a single document:**

1. Open your collection in Compass
2. Click **"Add data"** → **"Insert document"**
3. Edit the JSON in the editor (the `_id` field is auto-generated)
4. Click **"Insert"**

![Insert Document editor](images/compass-insert-document.png)

**Insert multiple documents:**

1. Click **"Add data"** → **"Insert document"**
2. Replace the `{}` with an array of documents:

```json
[{ "course": "Data Engineering" }, { "course": "Data Analysis" }]
```

3. Click **"Insert"**

---

### Adding Documents via mongosh

To insert data into our collection:

```mongosh
db.institute.insertOne({name: "New document"})
```

Add multiple documents in one command:

```mongosh
db.institute.insertMany([{"course": "Data Engineering"}, {"course": "Data Analysis"}])
```

How to view documents in a collection in mongosh:

```mongosh
db.institute.find()
```

![Collection view in Compass](images/compass-collection-view.png)

---

## Validation

MongoDB allows you to enforce rules on documents in a collection using **JSON Schema validation**. This ensures that only documents matching your defined structure can be inserted.

### Creating a Collection with Validation

The example below creates a `students` collection that requires every document to have a `name` (string) and an `age` (integer):

```mongosh
db.createCollection("students", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "age"],
      properties: {
        name: { bsonType: "string" },
        age: { bsonType: "int" }
      }
    }
  }
})
```

A successful output looks like:

![Validation collection created](images/validation-create-collection.png)

### Invalid Document

Attempting to insert a document that fails validation — here `age` is missing:

```mongosh
db.students.insertOne({ name: "Alice" })
```

MongoDB rejects the insert with a validation error:

![Invalid insert error](images/validation-invalid.png)

### Valid Document

Inserting a document that meets all the validation rules:

```mongosh
db.students.insertOne({ name: "Alice", age: 25 })
```

MongoDB confirms the insert was successful:

![Valid insert success](images/validation-valid.png)

---

## Working with a Films Collection

### Creating the Collection with Validation

The `films` collection requires every document to have a `title` (string), `year` (int), and `genre` (string):

```mongosh
db.createCollection("films", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["title", "year", "genre"],
      properties: {
        title: { bsonType: "string" },
        year: { bsonType: "int" },
        genre: { bsonType: "string" }
      }
    }
  }
})
```

![Films collection created](images/films-create-collection.png)

---

### Inserting Documents

**insertMany** — insert multiple documents in one command:

```mongosh
db.films.insertMany([
  { title: "Inception", year: 2010, genre: "Sci-Fi" },
  { title: "The Dark Knight", year: 2008, genre: "Action" },
  { title: "Interstellar", year: 2014, genre: "Sci-Fi" }
])
```

![insertMany output](images/films-insert-many.png)

**insertOne** — insert a single document:

```mongosh
db.films.insertOne({ title: "The Matrix", year: 1999, genre: "Sci-Fi" })
```

![insertOne output](images/films-insert-one.png)

**insert()** — the older deprecated method, still works but not recommended:

```mongosh
db.films.insert({ title: "Pulp Fiction", year: 1994, genre: "Crime" })
```

MongoDB will show a `DeprecationWarning` and recommend using `insertOne`, `insertMany`, or `bulkWrite` instead:

![insert() deprecation warning](images/films-insert-deprecated.png)

---

### Searching for Documents

**Find all documents** in a collection:

```mongosh
db.films.find()
```

![find() all documents](images/films-find-all.png)

**Filter by a field** — find all Sci-Fi films:

```mongosh
db.films.find({ genre: "Sci-Fi" })
```

Only documents matching the filter are returned:

![find() with filter](images/films-find-filter.png)

---

### Updating Documents

**updateOne** — update the first document that matches the filter. Here we correct the year for Inception:

```mongosh
db.films.updateOne({ title: "Inception" }, { $set: { year: 2011 } })
```

`matchedCount: 1` and `modifiedCount: 1` confirm one document was updated:

![updateOne output](images/films-update-one.png)

**updateMany** — update all documents that match the filter. Here we rename the genre for all Sci-Fi films:

```mongosh
db.films.updateMany({ genre: "Sci-Fi" }, { $set: { genre: "Science Fiction" } })
```

`matchedCount: 3` and `modifiedCount: 3` confirm all matching documents were updated:

![updateMany output](images/films-update-many.png)

---

### Deleting Documents

**deleteOne** — delete the first document that matches the filter:

```mongosh
db.films.deleteOne({ title: "Pulp Fiction" })
```

`deletedCount: 1` confirms the document was removed:

![deleteOne output](images/films-delete-one.png)

---

## Embedding vs Referencing

When designing a MongoDB database, one of the key decisions is how to handle **related data**. There are two main approaches: **embedding** and **referencing**.

---

### Embedding

Embedding means storing related data **directly inside a document** as a nested object or array.

```json
{
  "_id": "1",
  "name": "Alice Johnson",
  "address": {
    "street": "123 Main St",
    "city": "London",
    "postcode": "EC1A 1BB"
  },
  "courses": ["Data Engineering", "Data Analysis"]
}
```

**When to use embedding:**

- The nested data is always accessed together with the parent document
- The nested data doesn't change frequently
- The relationship is **one-to-few** (e.g. a user with a few addresses)
- You want fast reads — one query returns everything you need

**Advantages:**

- Single query to retrieve all related data
- No JOINs required
- Better read performance

**Disadvantages:**

- Documents can grow very large
- Duplicated data if the same nested data is shared across multiple documents
- Harder to update nested data across many documents

---

### Referencing

Referencing means storing related data in a **separate collection** and linking to it using an `_id` — similar to a foreign key in SQL.

```json
// users collection
{
  "_id": "1",
  "name": "Alice Johnson",
  "course_ids": ["101", "102"]
}

// courses collection
{
  "_id": "101",
  "title": "Data Engineering"
}
```

To retrieve the full data, you would need to query both collections.

**When to use referencing:**

- The related data is large or frequently updated
- The related data is shared across many documents
- The relationship is **one-to-many** or **many-to-many**
- You want to avoid data duplication

**Advantages:**

- Smaller, cleaner documents
- Easier to update shared data in one place
- Better for complex or large relationships

**Disadvantages:**

- Requires multiple queries to retrieve related data
- More complex application logic

---

### Summary

|                  | Embedding                | Referencing                  |
| ---------------- | ------------------------ | ---------------------------- |
| Data location    | Inside the document      | Separate collection          |
| Query complexity | Simple (one query)       | Complex (multiple queries)   |
| Best for         | One-to-few relationships | One-to-many / many-to-many   |
| Update ease      | Harder across documents  | Easier (update in one place) |
| Performance      | Faster reads             | Faster writes/updates        |

---

## PyMongo — Interacting with MongoDB via Python

**PyMongo** is the official Python driver for MongoDB. It lets you connect to a MongoDB database and perform CRUD operations using Python instead of the Mongo shell.

### Setup

```bash
pip install pymongo requests
```

### Star Wars Database

The Python scripts in this project fetch Star Wars data from the [SWAPI API](https://swapi.info/) and populate a `starwars` database in MongoDB, using **referencing** between collections (pilots stored as `_id` references rather than embedded objects).

Run each script to populate the corresponding collection:

```bash
python starships.py
python vehicles.py
python planets.py
python species.py
python films.py
```

> **Note:** `characters` must be pre-populated separately as it is referenced by all other collections.

### Querying with PyMongo

`queries.py` demonstrates common query patterns against the `characters` collection:

```python
import pymongo

client = pymongo.MongoClient()
db = client['starwars']

# Find one document
db.characters.find_one({"name": "Darth Vader"})

# Filter with projection
db.characters.find_one(
    {"name": "Darth Vader"},
    {"name": 1, "height": 1, "_id": 0}
)

# Iterate a cursor
for doc in db.characters.find({"eye_color": "yellow"}):
    print(doc["name"])

# Aggregation — average height of female characters
db.characters.aggregate([
    {"$match": {"gender": "female"}},
    {"$group": {"_id": "$gender", "avg_height": {"$avg": "$height"}}}
])
```

Run it with:

```bash
python queries.py
```

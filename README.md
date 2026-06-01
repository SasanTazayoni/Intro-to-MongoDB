# Intro to MongoDB

MongoDB is a document database that stores JSON-like documents, which allows you to store data with flexible schema and provides querying and aggregation tools for access and analysis.

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

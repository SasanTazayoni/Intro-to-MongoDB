# Intro to MongoDB

MongoDB is a **document-oriented NoSQL database** that stores data as flexible, JSON-like documents. Unlike traditional relational databases (like MySQL or PostgreSQL) that organise data into rigid rows and tables, MongoDB uses **collections** and **documents** — making it a natural fit for modern applications that deal with varied or frequently changing data.

### How does it compare to SQL?

| SQL Term   | MongoDB Equivalent | Description                           |
|------------|--------------------|---------------------------------------|
| Database   | Database           | A container for collections           |
| Table      | Collection         | A group of related documents          |
| Row        | Document           | A single record, stored as JSON/BSON  |
| Column     | Field              | A key-value pair within a document    |
| Primary Key| `_id`              | Auto-generated unique identifier      |

### What does a document look like?

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

> **Tip:** If the connection fails, make sure the MongoDB service is running. On Windows, check Services or run `mongod` in a terminal.

---

## Creating a Database and Collection

### Using MongoDB Compass

1. In the left panel, click **"+ Create database"**
2. Enter a **Database Name** (e.g. `sparta`) and an initial **Collection Name** (e.g. `institute`)
3. Click **"Create Database"**

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

**Insert multiple documents:**

1. Click **"Add data"** → **"Insert document"**
2. Replace the `{}` with an array of documents:

```json
[
  { "course": "Data Engineering" },
  { "course": "Data Analysis" }
]
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

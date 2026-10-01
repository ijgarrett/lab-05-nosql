db = db.getSiblingDB("bookstore");

db.authors.drop();
let authorsData = JSON.parse(fs.readFileSync("authors.json", "utf8"));
db.authors.insertMany(authorsData)

db.books.drop();
let booksData = JSON.parse(fs.readFileSync("books.json", "utf8"));
db.books.insertMany(booksData);

print("--- ALL AUTHORS ---");
printjson(db.authors.find().toArray());

print("--- ALL BOOKS ---");
printjson(db.books.find().toArray());

db.books.insertMany([
  {
    "title": "Stardust",
    "published_year": 1999,
    "author_ids": ["author_002"]
  },
  {
    "title": "Dune",
    "published_year": 1965,
    "author_ids": ["author_004"]
  }
]);

db.authors.insertOne({
  "_id": "author_004",
  "name": "Frank Herbert",
  "nationality": "American",
  "bio": {
    "short": "American science fiction author best known for the novel Dune.",
    "long": "Frank Patrick Herbert Jr. was an American science fiction author best known for the 1965 novel Dune and its five sequels."
  }
});

print("--- FILTERED BOOKS (author_001, author_004) ---");
printjson(db.books.find({ author_ids: { $in: ["author_001", "author_004"] } }).toArray());

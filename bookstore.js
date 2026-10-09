// Step 2: Switch to bookstore database
db = db.getSiblingDB("bookstore")

// Step 3: Load authors.json
// Drop existing authors collection
db.authors.drop()
// Read and parse authors.json
doc = JSON.parse(fs.readFileSync("authors.json", "utf8"))
// Insert authors into collection
db.authors.insertMany(doc)

// Step 4: Load books.json
// Drop existing books collection
db.books.drop()
// Read and parse books.json
doc = JSON.parse(fs.readFileSync("books.json", "utf8"))
// Insert books into collection
db.books.insertMany(doc)

// Step 5: List authors and books
// Display all authors
db.authors.find()
// Display all books
db.books.find()

// Step 6: Insert two new books
// Add two books with author_004
db.books.insertMany([
    {
        title: "The Hunger Games",
        published_year: 2008,
        author_ids: ["author_004"]
    },
    {
        title: "The Ballad of Songbirds and Snakes",
        published_year: 2020,
        author_ids: ["author_004"]
    }
])

// Step 7: Add missing authors
// Check if author_004 already exists
db.authors.findOne({ _id: "author_004" })

// Insert new author Suzanne Collins
db.authors.insertOne({
    _id: "author_004",
    name: "Suzanne Collins",
    nationality: "American",
    bio: {
        short: "Author of The Hunger Games series.",
        long: "Suzanne Collins is an American author best known for writing The Hunger Games series. She was born on August 10, 1962, in Hartford, Connecticut, and began her career writing for children's television shows. Her books often explore themes of survival, power, war, and social inequality. Before The Hunger Games, she wrote The Underland Chronicles, a fantasy series for young readers. Her work has gained worldwide popularity, with The Hunger Games becoming a bestselling series and inspiring several successful film adaptations."
    }
})

// Step 8: Filter books by a list of authors
// Find books by Neil Gaiman or Suzanne Collins
db.books.find({
    author_ids: {
        $in: ["author_002", "author_004"]
    }
})

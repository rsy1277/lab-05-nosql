
#!/usr/bin/env python3

#Import libraries
import os
import logging
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Read MongoDB credentials from environment variables
MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

def main():
    """Connect to MongoDB Atlas and display books grouped by author."""

    # Check that all environment variables are set
    if not all([MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, MONGODB_ATLAS_PWD]):
        logging.error("Missing MongoDB environment variables.")
        return

    client = None

    try:
        # Connect to MongoDB Atlas
        client = MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD
        )

        # Verify the connection
        client.admin.command("ping")
        logging.info("Connected to MongoDB Atlas successfully.")

        # Select database and collections
        db = client["bookstore"]
        authors = db["authors"]
        books = db["books"]

        # Select authors from original data and added data
        author_ids = ["author_002", "author_003", "author_004"]

        # Count how many selected authors exist in the database
        total_authors = authors.count_documents({
            "_id": {"$in": author_ids}
        })

        print(f"\nTotal authors: {total_authors}")

        # Loop through the selected authors
        for author_id in author_ids:

            # Find the author by ID
            author = authors.find_one({"_id": author_id})

            if author is None:
                logging.warning("Author %s not found.", author_id)
                continue

            # Print the author's name
            print(f"\n{author['name']}:")

            # Find all books linked to this author
            author_books = books.find({
                "author_ids": author["_id"]
            })

            # Print each book's title and publication year
            for book in author_books:
                print(f"  {book['title']} ({book['published_year']})")

    except PyMongoError as e:
        # Log MongoDB connection or query errors
        logging.error("MongoDB error: %s", e)

    finally:
        # Close the connection
        if client is not None:
            client.close()
            logging.info("MongoDB connection closed.")


# Execute main only when running this file directly
if __name__ == "__main__":
    main()

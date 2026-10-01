#!/usr/bin/env python3
"""
bookstore_report.py

Connects to MongoDB Atlas using PyMongo and generates a formatted inventory 
report listing books linked to specified authors.
"""

import logging
import os
import sys
import pymongo
from pymongo.errors import PyMongoError

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Read environment variables for Atlas credentials
MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")


def get_mongo_client() -> pymongo.MongoClient:
    """Constructs and returns a MongoClient connected to MongoDB Atlas using environment variables.

    Returns:
        pymongo.MongoClient: Active connection client to MongoDB Atlas.
    """
    if not all([MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, MONGODB_ATLAS_PWD]):
        logging.error("Missing MongoDB environment credentials.")
        raise ValueError(
            "Please ensure MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, and MONGODB_ATLAS_PWD are set."
        )

    logging.info("Connecting to MongoDB Atlas...")
    client = pymongo.MongoClient(
        MONGODB_ATLAS_URL,
        username=MONGODB_ATLAS_USER,
        password=MONGODB_ATLAS_PWD,
        serverSelectionTimeoutMS=5000,
    )
    return client


def generate_author_report(
    db: pymongo.database.Database, target_author_ids: list[str]
) -> None:
    """Queries the database for specific author IDs and prints a formatted report

    showing each author and their published books.

    Parameters:
        db (pymongo.database.Database): MongoDB database instance.
        target_author_ids (list[str]): List of author _id strings to query.
    """
    authors_col = db["authors"]
    books_col = db["books"]

    # Retrieve authors whose _id matches any in the target list
    authors = list(authors_col.find({"_id": {"$in": target_author_ids}}))
    print(f"\nAuthors: {len(authors)}\n")

    for author in authors:
        author_id = author.get("_id")
        author_name = author.get("name", "Unknown Author")
        print(f"{author_name}")

        # Find all books where this author's _id is listed in author_ids array
        linked_books = books_col.find({"author_ids": author_id})

        book_count = 0
        for book in linked_books:
            title = book.get("title", "Untitled")
            year = book.get("published_year", "N/A")
            print(f"  {title} ({year})")
            book_count += 1

        if book_count == 0:
            print("  (No books found)")
        print()


def main() -> None:
    """Main execution function for generating the bookstore report."""
    client = None
    # Include original authors author_002, author_003, and new author_004
    target_authors = ["author_002", "author_003", "author_004"]

    try:
        client = get_mongo_client()
        db = client["bookstore"]

        # Run report generation
        generate_author_report(db, target_authors)
        logging.info("Report generated successfully.")

    except PyMongoError as e:
        logging.error(f"MongoDB error occurred: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        if client:
            client.close()
            logging.info("MongoDB client connection closed.")


if __name__ == "__main__":
    main()

from pymongo import MongoClient, ASCENDING, TEXT

# Connect to local MongoDB
# Why localhost:27017? That's the default MongoDB address on your computer
client = MongoClient('mongodb://localhost:27017/')

# Create/access database named 'movie_streaming'
db = client['movie_streaming']

# Create collections (like tables in SQL)
movies_collection = db['movies']
users_collection = db['users']
watch_history_collection = db['watch_history']
reviews_collection = db['reviews']


def create_indexes():
    """
    Create indexes to make searches faster
    Why indexes? Like a book index - helps find data quickly
    """
    
    # Text index for searching movies by title, director, cast
    # Why TEXT index? MongoDB built-in feature for keyword search
    movies_collection.create_index([
        ('title', TEXT),
        ('director', TEXT),
        ('cast', TEXT)
    ], name='movie_search_index')
    
    # Regular indexes for faster queries
    # Why ASCENDING? Sorts data A to Z for quick lookup
    users_collection.create_index([('email', ASCENDING)], unique=True)
    watch_history_collection.create_index([('user_id', ASCENDING)])
    watch_history_collection.create_index([('movie_id', ASCENDING)])
    watch_history_collection.create_index([('timestamp', ASCENDING)])
    reviews_collection.create_index([('movie_id', ASCENDING)])
    reviews_collection.create_index([('user_id', ASCENDING)])
    
    print("All indexes created successfully!")


def get_db():
    """Return database connection"""
    return db